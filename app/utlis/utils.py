import secrets
import string
import aiosmtplib
from email.message import EmailMessage
import os
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
EMAIL_APP_PASS = os.getenv("EMAIL_PASS")

## function to generate password reset token 
def generate_reset_token(length=32): 
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

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
