import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(from_email, subject, body):
    if not all([from_email, subject, body]):  # Check if any parameter is None or empty
        raise ValueError("Email parameters cannot be None or empty")
        
    smtp_server = os.getenv('SMTPSERVER')
    smtp_port = int(os.getenv('SMTPPORT'))
    smtp_username = os.getenv('SMTPUSERNAME')
    smtp_password = os.getenv('SMTPPASSWORD')
    smtp_email = os.getenv('SMTPEMAIL')  # This is the email account used to send

    # Create message
    message = MIMEMultipart()
    message["From"] = smtp_email       # Sender (your SMTP account)
    message["To"] = from_email        # Recipient
    message["Subject"] = subject
    message["Reply-To"] = from_email  # Replies will go to the user's email

    # Encode the body text properly
    body_part = MIMEText(body.strip(), "plain", "utf-8")
    message.attach(body_part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
            return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise


