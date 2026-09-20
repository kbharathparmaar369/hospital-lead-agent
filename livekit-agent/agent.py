from datetime import datetime, timedelta
import json
import logging
import os
import requests
from dotenv import load_dotenv
from livekit.agents import function_tool

from livekit.agents import(
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
    inference
)

load_dotenv()

logger=logging.getLogger("hospital-agent")
N8N_BASE_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook")

class HospitalIntakeAgent(Agent):
    def __init__(self) -> None:
        today_str = datetime.now().strftime("%Y-%m-%d")
        super().__init__(
            instructions=f"""
            You are a friendly hospital receptionist AI answering appointment inquiry calls.
Today's date is {today_str}. Use this to correctly resolve relative dates 
like "tomorrow" or "next Monday" into actual calendar dates in YYYY-MM-DD 
format when calling check_availability.
Start every call with this disclaimer:
"Hi, thanks for calling. If this is a medical emergency, please hang up and 
call emergency services immediately. Otherwise, I can help you schedule an 
appointment."

Then, naturally collect the following from the patient through conversation:
- Their name
- Phone number
- Email
- Reason for visit
- Preferred department
- Preferred date

Once you have a preferred date, use the check_availability tool to see real 
open slots. The tool returns available slots with "ist_time" (already converted 
to Indian Standard Time, IST) and "start_time".

Always read 3-5 options from "ist_time" to the patient (for example: "We have openings 
at 9:30 AM, 10:00 AM, 11:30 AM, or 2:00 PM"). Never say UTC times.

IMPORTANT: When the patient confirms a slot, use the EXACT "start_time" 
associated with that chosen "ist_time" as the start_time parameter in create_booking.

Once you have all required information and the patient confirms a slot, 
call create_booking. Confirm the booking clearly at the end.

Keep your responses short and conversational, like a real phone call. 
Do not read this list back to the patient - just ask naturally, one or two 
things at a time.
            """
        )

    @function_tool()
    async def check_availability(self, preferred_date: str) -> str:
        """Check available appointment slots for a given date (format: YYYY-MM-DD)."""
        logger.info(f"checking availability for {preferred_date}")
        try:
            response = requests.post(
                f"{N8N_BASE_URL}/check-availability",
                json={
                    "preferred_date" : preferred_date
                },
                timeout = 10,
            )

            response.raise_for_status()
            raw_data = response.json()
            slots = raw_data.get("data", {}).get(preferred_date, [])
            
            if not slots:
                return f"No open appointment slots found for {preferred_date}."

            formatted_slots = []
            for slot in slots:
                raw_start = slot.get("start")
                if not raw_start:
                    continue
                try:
                    dt_utc = datetime.fromisoformat(raw_start.replace("Z", "+00:00"))
                    dt_ist = dt_utc + timedelta(hours=5, minutes=30)
                    ist_label = dt_ist.strftime("%I:%M %p").lstrip("0")
                    formatted_slots.append({
                        "ist_time": ist_label,
                        "start_time": raw_start
                    })
                except Exception:
                    formatted_slots.append({
                        "ist_time": raw_start,
                        "start_time": raw_start
                    })

            return json.dumps({
                "date": preferred_date,
                "timezone": "IST (Indian Standard Time)",
                "available_slots": formatted_slots
            })
        except Exception as e:
            logger.error(f"Check availability failed: {e}")
            return "I couldn't check availability right now. Please try again later."


    @function_tool()
    async def create_booking(
        self,
        patient_name: str,
        patient_phone: str,
        patient_email: str,
        reason: str,
        department: str,
        preferred_date: str,
        start_time: str,
    ) -> str:
        logger.info(f"Attempting to create booking for {patient_name}")
        
        try:
            response = requests.post(
                f"{N8N_BASE_URL}/create-booking",
                json={
                    "patient_name": patient_name,
                    "patient_phone": patient_phone,
                    "patient_email": patient_email,
                    "reason": reason,
                    "department": department,
                    "preferred_date": preferred_date,
                    "start_time": start_time,
                },
              timeout = 15,
            )
            response.raise_for_status()
            return "Booking confirmed successfully."

        except Exception as e:
            logger.error(f"create_booking failed : {e}") 
            return "I couldnt complete the booking , please try again or call the front desk."         
  

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    today_str = datetime.now().strftime("%Y-%m-%d")

    session = AgentSession(
        stt=inference.STT(model="deepgram/flux-general-en", language="en"),
        llm=inference.LLM(model="openai/gpt-4o-mini"),
        tts=inference.TTS(model="inworld/inworld-tts-2", voice="Ashley"),
    )

    await session.start(
        agent=HospitalIntakeAgent(),
        room=ctx.room,
    )

    await session.generate_reply(
        instructions="Greet the caller and deliver the emergency disclaimer, then ask how you can help."
    )


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="hospital-lead-agent",
        )
    )