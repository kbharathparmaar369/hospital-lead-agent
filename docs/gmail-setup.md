# Gmail SMTP Setup

Used for sending appointment confirmation emails via n8n.

## Setup Steps
1. Enable 2-Step Verification on your Google Account
2. Generate an App Password: Google Account → Security → App Passwords
3. In n8n, create SMTP credentials:
   - Host: smtp.gmail.com
   - Port: 587
   - User: your-email@gmail.com
   - Password: (App Password, not your real Gmail password)

## Note
Gmail's free SMTP has a sending limit (~500 emails/day) — fine for a 
demo, would need a dedicated transactional email service for production 
scale.