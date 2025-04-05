import re  
import requests  
from flask import Flask, render_template, request, jsonify  
import json  
import os 
from dotenv import load_dotenv 
from SMTP import send_email  

app = Flask(__name__)

load_dotenv()
HCAPTCHA_SECRET_KEY = os.getenv("SECRET_KEY")
valid_email_file = "email_list.json"

# Load valid domains from the JSON file
def load_valid_emails(valid_email_file):
    try:
        with open(valid_email_file, 'r') as file:
            emails = json.load(file)
            return set(emails.get("valid_domains", []))
    except Exception as e:
        print(f"Error loading emails: {e}")
        return set()

VALID_EMAILS = load_valid_emails(valid_email_file)

# Check if email's domain is valid
def is_valid_email(email):
    if "@" not in email:
        return False  
    email_domain = email.split('@')[-1].strip().lower()
    return email_domain in VALID_EMAILS  

# Check email format
def is_email_format_valid(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)  
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()
    privacy_check = request.form.get("privacyCheck")
    captcha_token = request.form.get("h-captcha-response")
    
    errors = {}

    # CAPTCHA check
    if not captcha_token or not verify_captcha(captcha_token).get('success'):
        errors["captcha"] = "CAPTCHA verification failed."

    # Required fields
    if not name:
        errors["name"] = "Name is required."

    if not email:
        errors["email"] = "Email is required."
    elif not is_email_format_valid(email):
        errors["email"] = "Invalid email format."
    elif not is_valid_email(email):
        errors["email"] = "Email domain is not allowed."

    if not subject:
        errors["subject"] = "Subject is required."

    if not message:
        errors["message"] = "Message is required."

    if not privacy_check:
        errors["privacyCheck"] = "You must agree to the privacy policy."

    if errors:
        return render_template("Contact.html", 
            errors=errors, 
            request=request, 
            sitekey=os.getenv("hcaptcha-sitekey"),
            captcha_token=captcha_token,
            form_data={  # Add form data to preserve input values
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
                'privacyCheck': privacy_check
            })

    # Everything passed — send email
    email_body = f"""
    You received a new message from your contact form:

    Name: {name}
    Email: {email}
    Subject: {subject}

    Message:
    {message}
    """

    try:
        send_email(subject=f"Contact Form: {subject}", body=email_body)
        
        # Return a success message and clear form fields by passing empty strings
        return render_template("Contact.html", 
            success="Thank you! Your message has been sent successfully.", 
            errors={},
            sitekey=os.getenv("hcaptcha-sitekey"),
            form_data={
                'name': '',
                'email': '',
                'subject': '',
                'message': '',
                'privacyCheck': False
            })
    except Exception as e:
        return render_template("Contact.html", 
            error=f"Error sending email: {str(e)}", 
            errors={},
            sitekey=os.getenv("hcaptcha-sitekey"),
            form_data=request.form)


# Verify hCaptcha
def verify_captcha(captcha_token):
    url = 'https://hcaptcha.com/siteverify'  
    data = {'secret': HCAPTCHA_SECRET_KEY, 'response': captcha_token}
    response = requests.post(url, data=data)  
    return response.json()  

@app.route('/Contact')
def Contact():
    sitekey = os.getenv("hcaptcha-sitekey")
    return render_template("Contact.html", 
        sitekey=sitekey, 
        errors={},
        form_data={
            'name': '',
            'email': '',
            'subject': '',
            'message': '',
            'privacyCheck': False
        })

@app.route('/Home')
def Home():
    return render_template("Index.html")

if __name__ == '__main__':
    app.run(debug=True)
