from flask import Flask, render_template, request
import json
import os
import re
import requests
from dotenv import load_dotenv
from SMTP import send_email 

app = Flask(__name__)
load_dotenv()

HCAPTCHA_SECRET_KEY = os.getenv("SECRET_KEY")
valid_email_file = "email_list.json"

def load_valid_emails(filepath):
    try:
        with open(filepath, 'r') as f:
            return set(json.load(f).get("valid_domains", []))
    except:
        return set()

VALID_EMAILS = load_valid_emails(valid_email_file)

def is_valid_email(email):
    domain = email.split('@')[-1].strip().lower()
    return domain in VALID_EMAILS

def is_email_format_valid(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

def verify_captcha(token):
    url = 'https://hcaptcha.com/siteverify'
    data = {'secret': HCAPTCHA_SECRET_KEY, 'response': token}
    return requests.post(url, data=data).json()

@app.route('/')
@app.route('/Home')
def Home():
    try:
        with open("cardwheel.json") as f:
            carousel_items = json.load(f)
            print("Carousel data loaded successfully.")
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

    if not captcha_token or not verify_captcha(captcha_token).get('success'):
        errors["captcha"] = "CAPTCHA verification failed."

    if not name: errors["name"] = "Name is required."
    if not email: errors["email"] = "Email is required."
    elif not is_email_format_valid(email): errors["email"] = "Invalid email format."
    elif not is_valid_email(email): errors["email"] = "Email domain is not allowed."
    if not subject: errors["subject"] = "Subject is required."
    if not message: errors["message"] = "Message is required."
    if not privacy_check: errors["privacyCheck"] = "Please accept privacy policy."

    if errors:
        return render_template("Contact.html", errors=errors,
            sitekey=os.getenv("hcaptcha-sitekey"),
            form_data={
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
                'privacyCheck': privacy_check
            })

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
            errors={}, form_data={'name': '', 'email': '', 'subject': '', 'message': '', 'privacyCheck': False})
    except Exception as e:
        return render_template("Contact.html", error=str(e),
            sitekey=os.getenv("hcaptcha-sitekey"),
            errors={}, form_data=request.form)

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)