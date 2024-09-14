import aiosmtplib
from email.message import EmailMessage

from dotenv import load_dotenv
import os

load_dotenv()

# SMTP_EMAIL = os.getenv("EMAIL")
# EMAIL_APP_PASS = os.getenv("PASSWORD")

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
EMAIL_APP_PASS = os.getenv("EMAIL_PASS")

# Set environment variables for email credentials

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
# SMTP_PASSWORD = os.getenv("SMTP_MAIL_PASS")
EMAIL_APP_PASS = os.getenv("EMAIL_APP_PASS_03")

print(f"smtp envs : {SMTP_EMAIL} and {EMAIL_APP_PASS} ")


# Function to send email
async def send_email(email: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = SMTP_EMAIL  # Sender email
    message["To"] = email  # Recipient email
    message["Subject"] = subject
    message.set_content(body)

    # Using aiosmtplib for async SMTP
    await aiosmtplib.send(message, hostname="smtp.gmail.com", port=587, start_tls=True,
                          username=SMTP_EMAIL, password=EMAIL_APP_PASS)
