# Known Limitations (Demo Scope)

- **Single department/calendar**: Cal.com free tier supports one 
  user/calendar. The "department" field is currently informational only 
  (logged to Supabase) and does not route to different calendars. A 
  production system would use Cal.com Teams (paid) with a department → 
  event-type routing step in n8n.
- **No automated urgency detection**: rather than having the AI agent 
  make triage decisions, the agent gives a spoken disclaimer directing 
  emergencies to call emergency services directly. This is a deliberate 
  safety choice, not a missing feature.
- **Local-only deployment**: this project runs n8n locally (not hosted) 
  due to free-tier hosting constraints (sleep-on-idle, no persistent 
  disk, blocked SMTP ports). See README for details.