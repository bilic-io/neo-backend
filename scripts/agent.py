from typing import Optional, Dict, Callable, Awaitable
from typing import Optional
from browser_use import Agent, Browser, BrowserConfig, Controller, ActionResult
from langchain_openai import ChatOpenAI
import asyncio
import logging
from typing import Optional, Callable, Awaitable
from browser_use import Controller, ActionResult
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

sender_email = os.getenv("EMAIL_HOST_USER")
sender_password = os.getenv("EMAIL_HOST_PASSWORD")
smtp_server = os.getenv("EMAIL_HOST")
smtp_port = int(os.getenv("EMAIL_PORT"))

logging.getLogger("browser_use").setLevel(logging.DEBUG)

custom_system_prompt = """
You are an advanced autonomous browser agent with self-determining monitoring capabilities. Your operational protocol:

After extracting content or completing significant actions, always invoke the 'Send update' action with a relevant message describing the action taken or data extracted.

Always consistently send an update back by calling the 'send update' action with a message or clean data extracted structure it properly.

use the 'send email' action to send emails to users when necessary this is determined by you two parameters are needed for the send email action 1. recipient  2. message.
Ensure that updates are sent consistently to keep the user informed about the progress.

1. Parameter Determination:
- Analyze task urgency and type to set initial check interval:
- Set maximum duration based on task nature:

2. Initialization Sequence:
- Send immediate task confirmation
- Send constant updates at intervals when new data or information relevant to the task is available
- Explain monitoring rationale

3. Adaptive Adjustment:
- Modify intervals based on:
  - Observed pattern changes
  - Time of day
  - Historical response times
- Communicate parameter changes via:
  [ADJUSTED_INTERVAL: New minutes]

4. Update Protocol:
- Include time since last update
- Maintain session state between checks
- Handle authentication persistence

Example initialization:
\"\"\"
TASK_INITIATED: Job status monitoring
[INTERVAL: 45 minutes]
[DURATION: 72 hours]
Rationale: Standard office hours check pattern
Next update at {next_check_time}
\"\"\"
"""

async def kickStartBrowser(
    task: str,
    update_callback: Optional[Callable[[str], Awaitable[None]]] = None,
    model: str = "gpt-3.5-turbo"
):
    print("browser initializing ================")
    browser = Browser(config=BrowserConfig(headless=False, disable_security=True))
    print("browser successfully initialized ================")
    llm = ChatOpenAI(model=model, temperature=0.0)
    print("llm initialized ================")
    
    # Create a new controller instance per agent
    controller = Controller()
    
    # Register the send_update action with access to update_callback
    @controller.action('Send update')
    async def send_update(message: str):
        print("controller triggered this....")
        if update_callback:
            await update_callback(message)
        # The original script had a placeholder for send_email here. 
        # We will call the send_email action directly from the agent's task.
        return ActionResult(extracted_content="Update sent")
    
    # Register the send_email action
    @controller.action('Send email')
    async def send_email_action(recipient: str, message: str):
        print(f"Controller triggered send email to {recipient} with message: {message}")
        try:
            send_email(recipient, message)
            return ActionResult(extracted_content="Email sent successfully")
        except Exception as e:
            return ActionResult(extracted_content=f"Failed to send email: {e}")
    
    agent = Agent(
        task=task,
        llm=llm,
        use_vision=False,
        browser=browser,
        controller=controller,
        message_context=custom_system_prompt 
    )
    
    try:
        print("preparing to run agent ================")
        result = await agent.run()
    finally:
        await browser.close()
    
    return result

def send_email(recipient, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = "US Visa Appointment Update"

    msg.attach(MIMEText(message, 'plain'))

    # Use SSL instead of TLS
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient, text)
    server.quit()

async def monitor_visa_appointments():
    # --- User Configuration ---
    VISA_APPOINTMENT_URL = os.getenv("VISA_APPOINTMENT_URL")
    USER_EMAIL = os.getenv("USER_EMAIL")
    USER_PASSWORD = os.getenv("USER_PASSWORD")
    TARGET_CONSULATE = os.getenv("TARGET_CONSULATE")
    LOGIN_PAGE = os.getenv("LOGIN_PAGE")
    RECIPIENT_EMAIL_FOR_NOTIFICATIONS = os.getenv("RECIPIENT_EMAIL_FOR_NOTIFICATIONS")
    # --------------------------

    task_description = f"""
    Navigate to {VISA_APPOINTMENT_URL}. 
    If redirected to a login page ({LOGIN_PAGE}), 
    enter '{USER_EMAIL}' into the email field and '{USER_PASSWORD}' into the password field. 
    Click the checkbox for 'I have read and understood the Privacy Policy and the Terms of Use'. 
    Then click the 'Sign In' button. 
  
    On the appointment scheduling page, select '{TARGET_CONSULATE}' from the 'Consular Section Location' dropdown. 
    Then click the 'Schedule Appointment' button. 
    If you encounter a 'System is busy. Please try again later.' message, send an update saying 'No appointments available in {TARGET_CONSULATE} at this time.' and use the 'Send email' action to send an email to '{RECIPIENT_EMAIL_FOR_NOTIFICATIONS}' with the message 'No available US Visa Appointment in {TARGET_CONSULATE} at this time.'

    Otherwise, if you see any indication of available dates (e.g., a calendar, specific date text), 
    extract the relevant information about the available dates and use the 'Send email' action to send an email to '{RECIPIENT_EMAIL_FOR_NOTIFICATIONS}' 
    with the message containing the extracted date information. 
    Also, send an update message indicating that appointments are available and an email has been sent.
    """

    await kickStartBrowser(task=task_description)

if __name__ == "__main__":
    # send_email("secdad1@gmail.com", "Hello, this is a test email");
    asyncio.run(monitor_visa_appointments())