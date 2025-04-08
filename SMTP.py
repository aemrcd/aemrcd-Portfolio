import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")  
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))  
SMTP_EMAIL = os.getenv("SMTP_USERNAME") 
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")  

def send_email(to_email, subject, body):
    """
    Sends an email to a specific recipient using the configured SMTP server.

    :param to_email: Recipient email address (from user input)
    :param subject: Subject of the email
    :param body: Body of the email
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
        raise e
