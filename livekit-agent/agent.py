from livekit.protocol.agent_pb.agent_session import AgentSessionEvent
from livekit.agents.llm.chat_context import Instructions
import logging
from dotenv import load_dotenv

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

class HospitalIntakeAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""
            You are a friendly hospital receptionist AI answering appointment inquiry calls.

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
            - Preferred date/time

            Keep your responses short and conversational, like a real phone call. 
            Do not read this list back to the patient - just ask naturally, one or two 
            things at a time.
            
            """
        )


async def entrypoint(ctx: JobContext):
    await ctx.connect()

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