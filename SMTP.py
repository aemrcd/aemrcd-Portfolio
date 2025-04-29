
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load .env for local development (skip in production on Render)
load_dotenv()  # Only works locally


def send_email(from_email, subject, body):
    # Get SMTP credentials from environment variables
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = smtp_email  # Email you are sending from
    msg['To'] = smtp_email    # Send it to yourself (your email)
    msg['Subject'] = subject  # Email subject
    msg['Reply-To'] = from_email  # Set the "Reply-To" field to the user's email
    msg.attach(MIMEText(f"From: {from_email}\n\n{body}", 'plain'))  # Email body

    try:
        # Establish SMTP connection and send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(smtp_email, smtp_password)  # Log in with SMTP credentials
        server.send_message(msg)  # Send the message
        server.quit()  # Close the connection
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise


