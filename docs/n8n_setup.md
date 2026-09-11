# n8n Local Setup

This project runs n8n locally via npm (no Docker/hosting required for development).

## Install
npm install n8n -g

## Run
Set environment variables (optional, for basic auth):

export N8N_BASIC_AUTH_ACTIVE=true
export N8N_BASIC_AUTH_USER=your-username
export N8N_BASIC_AUTH_PASSWORD=your-password
export GENERIC_TIMEZONE=Asia/Kolkata

Then start n8n:

n8n

## Access
Open http://localhost:5678 in your browser.

## Data Storage
n8n stores workflows and credentials locally at `~/.n8n` by default — 
this persists automatically between runs on the same machine.

## Note
For a hosted/production deployment, see `docs/deployment-notes.md` 
for known limitations of free-tier hosting options.