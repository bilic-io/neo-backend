# Visa Appointment Monitoring Agent 🕵️‍♂️📧

This project implements an autonomous agent that monitors a specified webpage (such as a US Visa appointment portal) and sends email notifications when appointment statuses or relevant data change. It leverages browser automation, OpenAI's language models, and environment-based configuration for secure and adaptive monitoring.

## 🌐 What does it do?

- Monitors a target webpage (e.g., US Visa appointment site) for changes or available slots
- Handles login and navigation automatically
- Sends real-time email notifications to users when appointments become available or when status changes
- Provides adaptive monitoring intervals and session management
- Keeps users informed with constant updates and rationale for monitoring intervals

## 📋 Project Overview

This agent uses browser automation and AI to:
- Log in to a secure portal (with credentials from environment variables)
- Periodically check for appointment availability or other changes
- Send email alerts to a configured recipient when:
  - No appointments are available
  - New appointments or relevant data are found
- Adapt its monitoring frequency based on time of day, urgency, and historical patterns

## 🎯 Features

- Automated login and navigation
- Adaptive monitoring intervals
- Email notifications for status changes
- Secure configuration via `.env` file
- Session and authentication persistence

## 🛠️ Technical Stack

- Python
- Selenium (for browser automation)
- FastAPI (for API/websocket interface)
- LangChain + OpenAI GPT (for agent logic)
- browser-use agent
- dotenv (for environment variable management)

## 🚀 Getting Started

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_openai_key
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=465
   VISA_APPOINTMENT_URL=
   USER_EMAIL=your_portal_email
   USER_PASSWORD=your_portal_password
   TARGET_CONSULATE=Your Consulate
   LOGIN_PAGE=
   RECIPIENT_EMAIL_FOR_NOTIFICATIONS=notifyme@example.com
   ```
5. Run the agent:
   ```bash
   python scripts/agent.py
   ```
   Or start the API server:
   ```bash
   python scripts/api.py
   ```

## 📝 Note

- Keep your API keys and credentials secure. Never commit your `.env` file to version control.
- The `.gitignore` file is configured to exclude sensitive information.

## 📄 License

This project is open-source and available under the MIT License. 