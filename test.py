# Test script
from SMTP import send_email

try:
    send_email(
        to_email="recipient@example.com",
        subject="Test Email",
        body="This is a test email"
    )
    print("Test successful!")
except Exception as e:
    print(f"Test failed: {str(e)}")