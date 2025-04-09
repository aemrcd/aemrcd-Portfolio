import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(to_email, subject, body):
    # Get credentials from env
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_email = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    # Create message
    msg = MIMEMultipart()
    msg['From'] = to_email
    msg['To'] = smtp_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Create server object and secure the connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()  # Identify ourselves to the SMTP server
        server.starttls()  # Enable TLS encryption
        server.ehlo()  # Re-identify ourselves over TLS connection
        
        # Login and send
        server.login(smtp_email, smtp_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {to_email}")
            
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise