# Cal.com Setup

This project uses Cal.com Cloud (free tier) for appointment scheduling.

## Setup Steps
1. Create a free account at cal.com
2. Create an Event Type (e.g., "General Consultation") with duration 
   and availability hours configured
3. Note the Event Type ID (found in the event type's URL or via API)
4. Generate an API key: Settings → Developer → API Keys

## Environment Variables Needed
CALCOM_API_KEY=your-api-key
CALCOM_EVENT_TYPE_ID=your-event-type-id

## API Test
Confirm the key works:

curl --request GET \
  --url https://api.cal.com/v2/bookings \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "cal-api-version: 2026-05-01"


## Booking Page
Public booking link: cal.com/yourusername/general-consultation

## Note
Free tier supports one user/calendar. For multi-doctor/multi-department 
scheduling, a paid Teams plan would be required.