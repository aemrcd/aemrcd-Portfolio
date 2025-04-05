import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")  # e.g., "smtp.gmail.com"
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))  # Default to 587 for TLS
SMTP_EMAIL = os.getenv("SMTP_EMAIL")  # Your email address
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Your email password
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")  # Email to receive the form submission

def send_email(subject, body):
    """
    Sends an email using the configured SMTP server.

    :param subject: Subject of the email
    :param body: Body of the email
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")