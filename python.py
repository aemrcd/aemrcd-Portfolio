import smtplib
from flask import Flask, render_template, request
import os
import requests
from dotenv import load_dotenv
from SMTP import send_email
from smtplib import SMTPRecipientsRefused
import json

app = Flask(__name__)
load_dotenv()

HCAPTCHA_SECRET_KEY = os.getenv("SECRET_KEY")

# Verify CAPTCHA response
def verify_captcha(token):
    url = 'https://hcaptcha.com/siteverify'
    data = {'secret': HCAPTCHA_SECRET_KEY, 'response': token}
    return requests.post(url, data=data).json()

def verify_email_address(email):
    api_key = os.getenv("ABSTRACT_API_KEY")
    url = f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Debugging: Print the full response from AbstractAPI
        print(f"AbstractAPI response for {email}: {data}")
        
        # Check if the email is deliverable and not disposable
        deliverability = data.get("deliverability")
        is_disposable = data.get("is_disposable_email", {}).get("value", False)  # Fix this line

        print(f"Deliverability: {deliverability}, Is disposable: {is_disposable}")

        # Check for deliverability and that it's not a disposable email
        if deliverability == "DELIVERABLE" and not is_disposable:
            return True
        else:
            return False

    except Exception as e:
        print(f"Email validation error: {str(e)}")
        return False

@app.route('/')
@app.route('/Home')
def Home():
    try:
        with open("cardwheel.json") as f:
            carousel_items = json.load(f)
    except Exception as e:
        print(f"Error loading carousel data: {e}")
        carousel_items = []
    return render_template("Index.html", carousel_items=carousel_items)

@app.route('/Contact')
def Contact():
    return render_template("Contact.html", 
        sitekey=os.getenv("hcaptcha-sitekey"),
        errors={}, 
        form_data={'name': '', 'email': '', 'subject': '', 'message': '', 'privacyCheck': False})

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()
    privacy_check = request.form.get("privacyCheck")
    captcha_token = request.form.get("h-captcha-response")

    errors = {}

    # Validate CAPTCHA
    if not captcha_token or not verify_captcha(captcha_token).get('success'):
        errors["captcha"] = "CAPTCHA verification failed."

    # Validate Name
    if not name: 
        errors["name"] = "Name is required."

    # Validate Email
    if not email: 
        errors["email"] = "Email is required."
    elif not verify_email_address(email):  # Use AbstractAPI to check deliverability and non-disposable status
        errors["email"] = "This email doesn't appear to exist or is disposable. Please check for typos."

    # Validate Privacy Check
    if not privacy_check: 
        errors["privacyCheck"] = "Please accept privacy policy."

    if errors:
        return render_template("Contact.html", errors=errors,
            sitekey=os.getenv("hcaptcha-sitekey"),
            form_data=request.form)

    email_body = f"""
    You received a new message from your contact form:

    Name: {name}
    Email: {email}
    Subject: {subject}

    Message:
    {message}
    """

    try:
        send_email(to_email=email, subject=f"Contact Form: {subject}", body=email_body)
        return render_template("Contact.html", success="Thank you! Message sent.",
            sitekey=os.getenv("hcaptcha-sitekey"),
            errors={}, 
            form_data={'name': '', 'email': '', 'subject': '', 'message': '', 'privacyCheck': False})
    
    except SMTPRecipientsRefused:
        errors["email"] = "The email account does not exist. Please check the address."
        return render_template("Contact.html", 
            sitekey=os.getenv("hcaptcha-sitekey"),
            errors=errors,
            form_data=request.form)
    
    except smtplib.SMTPException as e:
        error_msg = str(e)
        if any(code in error_msg for code in ['550', '551', '554', 'NoSuchUser']):
            errors["email"] = "The email address does not exist or was rejected by the server."
        else:
            errors["general"] = "Email service is temporarily unavailable. Please try again later."
        return render_template("Contact.html",
            sitekey=os.getenv("hcaptcha-sitekey"),
            errors=errors,
            form_data=request.form)
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        errors["general"] = "An unexpected error occurred. Please try again later."
        return render_template("Contact.html",
            sitekey=os.getenv("hcaptcha-sitekey"),
            errors=errors,
            form_data=request.form)

if __name__ == '__main__':
    app.run(debug=True)
