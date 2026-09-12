# Cal.com Setup

This project uses Cal.com Cloud (free tier, API v2) for appointment scheduling.

## Setup Steps
1. Create a free account at cal.com
2. Create an Event Type (e.g., "health consultancy") with duration and 
   availability hours configured
3. Generate an API key: Settings → Developer → API Keys (starts with `cal_live_`)

## Environment Variables Needed
CALCOM_API_KEY=your-api-key
CALCOM_USERNAME=your-cal-username
CALCOM_EVENT_SLUG=your-event-slug
CALCOM_EVENT_TYPE_ID=your-numeric-event-type-id

## Important: API v2 Version Headers
Cal.com's v2 API requires a `cal-api-version` header, and different 
endpoints require DIFFERENT version values:

| Endpoint | cal-api-version |
|---|---|
| GET /v2/event-types | 2024-06-14 |
| GET /v2/slots | 2024-09-04 |
| POST /v2/bookings | 2024-08-13 |

Note: API v1 was fully shut down April 8, 2026 — v2 is required.

## API Tests

Get event types:
curl -X GET "https://api.cal.com/v2/event-types?username=YOUR_USERNAME" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "cal-api-version: 2024-06-14"

Check available slots:
curl -X GET "https://api.cal.com/v2/slots?eventTypeSlug=YOUR_SLUG&username=YOUR_USERNAME&start=2026-09-15&end=2026-09-16" \
  -H "cal-api-version: 2024-09-04"

## Booking Page (manual fallback)
cal.com/YOUR_USERNAME/YOUR_SLUG

## Note
Free tier supports one user/calendar. For multi-doctor/multi-department 
scheduling, a paid Teams plan would be required.