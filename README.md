# 🏥 Hospital Lead Agent — AI Voice Receptionist

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LiveKit](https://img.shields.io/badge/LiveKit-Agents-orange)
![n8n](https://img.shields.io/badge/n8n-Workflow%20Automation-red)
![Cal.com](https://img.shields.io/badge/Cal.com-API%20v2-black)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-emerald)
![License](https://img.shields.io/badge/License-MIT-green)

**An AI voice agent that answers hospital appointment calls, checks real doctor availability, and books consultations — hands-free, end-to-end.**

Built as a complete proof-of-concept for automating routine hospital front-desk scheduling using a real-time voice AI pipeline (LiveKit) orchestrated through n8n, live calendar scheduling via Cal.com, lead tracking in Supabase, and email dispatch via Gmail SMTP.

[Features](#-features) • [How It Works](#-how-it-works) • [Architecture](#-architecture) • [Full Launch Procedure](#-complete-step-by-step-launch-procedure) • [Tech Stack](#-tech-stack) • [Skills Demonstrated](#-skills-demonstrated)

---

## 📌 Overview

Hospitals lose time and patients to manual phone intake — routine appointment requests tie up front-desk staff, and calls get missed during busy hours. **Hospital Lead Agent** is an AI receptionist that picks up, conducts a natural spoken conversation, checks a doctor's live calendar, books the chosen slot, logs the patient lead to a database, and sends an immediate confirmation email — all without human intervention.

This repository includes:
1. **LiveKit Voice Agent** (`livekit-agent/agent.py`) with STT (Deepgram), LLM (GPT-4o-mini), and TTS (Inworld), dynamically converting raw calendar slots into Indian Standard Time (IST).
2. **n8n Orchestration Workflows** (`n8n/workflows/`) handling slot checks, Cal.com bookings, Supabase database storage, and Gmail confirmation emails.
3. **Interactive Hospital Website** (`index.html`) featuring a floating 24/7 AI Receptionist phone widget with animated pulse waves and one-click voice calling.

---

## ✨ Features

### 🎤 Real Voice Conversation
- Natural spoken conversation via **LiveKit Agents** (STT → LLM → TTS)
- Opens every call with a safety disclaimer directing emergencies to call emergency services directly
- Naturally collects patient name, contact info, reason for visit, and preferred date/time

### 📅 Real Scheduling, Not a Mock
- Checks **actual live availability** on a real Cal.com calendar using Cal.com API v2
- Automatically converts raw UTC calendar timestamps to **Indian Standard Time (IST, UTC+5:30)** before speaking options (e.g. *"9:30 AM, 10:00 AM, 11:30 AM"*)
- Books the exact slot chosen by the patient — no hallucinated or guessed times

### 🔁 Full Automation Pipeline
- **n8n** orchestrates the complete backend flow: availability checking → booking creation → lead logging → email confirmation
- Every patient lead is recorded into **Supabase PostgreSQL** with a linked Cal.com booking ID
- Automated HTML confirmation email dispatched via **Gmail SMTP**

### 🌐 Embeddable Phone Widget & Hospital Site
- Includes a hospital website (`index.html`) with an interactive floating phone action button
- Embeds the LiveKit voice interface directly inside a sleek modal with microphone access

---

## 🖥️ Example Call

```text
🤖 Agent: "Hi, thanks for calling. If this is a medical emergency, please hang up and 
          call emergency services immediately. Otherwise, I can help you schedule an 
          appointment. How can I help?"

👤 Patient: "Hi, I have a persistent headache and fever, I need to see a doctor."

🤖 Agent: "I'm sorry to hear that. Could I get your name, phone number, and email?"

👤 Patient: "Rahul Sharma, 9876543210, rahul@example.com."

🤖 Agent: "Thanks Rahul. Which date works best for your consultation?"

👤 Patient: "September 22nd if possible."

🤖 Agent: "Let me check our calendar... We have openings at 9:30 AM, 10:00 AM, 10:30 AM, 
          and 11:00 AM. Which one works best for you?"

👤 Patient: "10:00 AM works."

🤖 Agent: "You're all set, Rahul! Your appointment for General Medicine on September 22nd 
          at 10:00 AM is confirmed. We have sent a confirmation email with all details. 
          Is there anything else I can help you with?"
```

---

## 🏗️ Architecture

```text
       Patient (Speaks into Browser / Phone Widget)
                          │
                          ▼
       LiveKit Voice Agent (STT → LLM → TTS)
           │
           │  Function Tools: check_availability, create_booking
           ▼
       n8n Automation Engine (Runs Locally)
           │
           ├───► Cal.com API v2  ──► Query Live Slots & Create Booking
           ├───► Supabase (PostgreSQL) ──► Store Patient Lead Record
           └───► Gmail SMTP ──► Send Immediate Confirmation Email
```

---

## 🛠️ Tech Stack

| Component | Technology | Role |
|---|---|---|
| **Voice Agent** | LiveKit Agents Python SDK | Real-time WebRTC audio loop & orchestration |
| **Speech-to-Text (STT)** | Deepgram (`flux-general-en`) | Ultra-low latency voice transcription |
| **Reasoning (LLM)** | OpenAI (`gpt-4o-mini`) | Conversational triage & function tool execution |
| **Text-to-Speech (TTS)** | Inworld (`inworld-tts-2`, Ashley) | Natural, expressive spoken voice |
| **Automation** | n8n | Webhook routing, API translation, and alerting |
| **Calendar Scheduling**| Cal.com (API v2) | Live slot availability and automated booking |
| **Database** | Supabase (PostgreSQL) | Persistent patient leads and triage logs |
| **Email Delivery** | Google SMTP | Patient appointment confirmations |
| **Web Frontend** | HTML5, CSS3, JavaScript | Hospital landing page & floating phone widget |
| **Web Embed Starter** | Next.js 15, React 19, LiveKit Client | WebRTC client inside iframe widget |

---

## 🚀 Complete Step-by-Step Launch Procedure

Follow these steps to run the entire system locally:

### Prerequisites
- **Python 3.11+** installed
- **Node.js (v18+)** and `npm` installed
- Accounts: [LiveKit Cloud](https://cloud.livekit.io), [Cal.com](https://cal.com), [Supabase](https://supabase.com), and Gmail with an App Password.

---

### Step 1: Clone Repository & Configure Root `.env`
```powershell
git clone https://github.com/kbharathparmaar369/hospital-lead-agent.git
cd hospital-lead-agent
```

Create a `.env` file in the root folder with your credentials:
```env
# LiveKit Cloud Credentials
LIVEKIT_URL=wss://<your-project>.livekit.cloud
LIVEKIT_API_KEY=<your-api-key>
LIVEKIT_API_SECRET=<your-api-secret>

# Cal.com
CALCOM_API_KEY=cal_live_...
CALCOM_EVENT_TYPE_ID=...

# Supabase
SUPABASE_URL=https://<your-project-ref>.supabase.co
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...

# Gmail SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-16-char-google-app-password
```

---

### Step 2: Start n8n & Import Workflows
1. Install and launch n8n locally:
   ```powershell
   npm install n8n -g
   n8n
   ```
2. Open **`http://localhost:5678`** in your browser.
3. Import the two workflows from the `n8n/workflows/` folder:
   - `n8n/workflows/availability-check.json`
   - `n8n/workflows/create-booking.json`
4. Set up your Gmail credentials under **Credentials** in n8n.
5. Activate both workflows.

*(See [docs/n8n_setup.md](docs/n8n_setup.md) for full n8n configuration instructions).*

---

### Step 3: Run the LiveKit Voice Agent
Open a **new terminal**:
```powershell
cd livekit-agent

# Activate virtual environment (or create with python -m venv venv)
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Start the LiveKit voice worker
python agent.py dev
```
You should see:
```text
INFO livekit.agents - registered worker {"agent_name": "hospital-lead-agent", ...}
```

---

### Step 4: Run the Next.js Web Embed Server
Open a **new terminal**:
```powershell
cd livekit-agent\agent-starter-embed

# Configure environment if not already done
# Ensure .env contains your LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET

# Start Next.js development server
npm run dev
```
The embed client will start on **`http://localhost:3000`**.

---

### Step 5: Launch the Hospital Website with Floating Phone Widget
Open a **new terminal**:
```powershell
# From the project root folder
python -m http.server 8080
```
Open **`http://localhost:8080/index.html`** in Chrome, Edge, or Firefox.

1. Click the glowing **Phone Icon** in the bottom-right corner (or click any *"Book Appointment"* button).
2. The AI Receptionist modal will open. Click **"CHAT WITH AGENT"**.
3. Allow microphone permissions when prompted.
4. Speak naturally to book your consultation!

---

## 🧪 Testing the Webhooks Directly

You can test both n8n endpoints using `curl`:

#### Test 1: Check Availability
```bash
curl -X POST http://localhost:5678/webhook/check-availability \
  -H "Content-Type: application/json" \
  -d '{"preferred_date": "2026-09-22"}'
```

#### Test 2: Create Booking
```bash
curl -X POST http://localhost:5678/webhook/create-booking \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "Rahul Sharma",
    "patient_email": "your-email@gmail.com",
    "patient_phone": "9876543210",
    "reason": "Health checkup",
    "department": "General Medicine",
    "start_time": "2026-09-22T04:30:00.000Z"
  }'
```

## 💡 Skills Demonstrated
- **Voice AI pipeline design**: STT / LLM / TTS orchestration via LiveKit Agents
- **Workflow automation & API integration**: n8n workflows connecting REST endpoints
- **Prompt engineering**: Structured conversational intake, entity extraction & tool-calling
- **Debugging distributed systems**: API versioning (Cal.com v2), timezone handling (UTC to IST), async error handling
- **Database design**: Supabase / PostgreSQL schema with row-level security
- **Documentation & honest scoping**: Known limitations, failure boundaries, and production tradeoffs

---

## ⚠️ Known Limitations

This is an end-to-end proof-of-concept. See [docs/known-limitations.md](docs/known-limitations.md) for details on:
- Single-calendar/event-type routing under Cal.com free tier.
- Deliberate emergency disclaimer instead of AI-based medical triage.
- Local n8n hosting considerations.

## 📄 Disclaimer

This project is a technical prototype demonstrating the integration of real-time voice AI with scheduling APIs. It is not a certified medical device. Real-world deployment in a clinical environment requires HIPAA compliance, clinical protocols, and doctor oversight.

---

**Developed by K Bharath Parmar**