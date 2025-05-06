import smtplib
from flask import Flask, render_template, request
import os
import requests
import json
import secrets  
from dotenv import load_dotenv
from SMTP import send_email
from smtplib import SMTPRecipientsRefused
from Connect_Database import connect_to_database

app = Flask(__name__)
load_dotenv()

HCAPTCHA_SECRET_KEY = os.getenv("SECRET_KEY")

# Verify CAPTCHA response
def verify_captcha(token):
    url = 'https://hcaptcha.com/siteverify'
    data = {'secret': HCAPTCHA_SECRET_KEY, 'response': token}
    response = requests.post(url, data=data).json()
    # print(f"CAPTCHA verification response: {response}")  # Debugging: Print the CAPTCHA response
    return response


def verify_email_address(email):
    api_key = os.getenv("ABSTRACT_API_KEY")
    url = f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}"
    
    allowed_free_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]

    try:
        response = requests.get(url)
        data = response.json()

        # Debugging: Print the full API response
        print(f"AbstractAPI response for {email}: {data}")

        # Get key validation metrics
        quality_score = float(data.get("quality_score", 0))
        is_valid_format = data.get("is_valid_format", {}).get("value", False)
        deliverability = data.get("deliverability", "UNDELIVERABLE")
        domain = email.split('@')[-1] if '@' in email else None

        # Log validation details
        print(f"Quality Score: {quality_score}, Valid Format: {is_valid_format}, "
              f"Deliverability: {deliverability}, Domain: {domain}")

        # Primary validation checks
        if not is_valid_format:
            print("Failed: Invalid email format")
            return False

        if quality_score < 0.80:  # acceptable quality score
            print("Failed: Low quality score")
            return False

        if deliverability != "DELIVERABLE":
            print("Failed: Not deliverable")
            return False

        # Check for allowed free domains
        if domain not in allowed_free_domains:
            print("Passed: Allowed free domain")
            return False

        # Accept any email that passed the above validations
        print("Passed: Valid email")
        return True

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
    email_is_valid = verify_email_address(email)
    if not email:
        errors["email"] = "Email is required."
    elif not email_is_valid:
        errors["email"] = "Invalid or disposable email address."

    # Validate Privacy Check
    if not privacy_check:
        errors["privacyCheck"] = "Please accept the privacy policy."

    # Stop early if there are errors
    if errors:
        return render_template("Contact.html",
            sitekey=os.getenv("hcaptcha-sitekey"),
            errors=errors,
            form_data=request.form)

    # Safety net: Recheck email validity before DB insert
    if not email_is_valid:
        errors["email"] = "Invalid email address (internal check)."
        return render_template("Contact.html",
            sitekey=os.getenv("hcaptcha-sitekey"),
            errors=errors,
            form_data=request.form)

    email_body = f"""
    You received a new message from your contact form:

    Name: {name}
    Email: {email}
    Subject: {subject}

    Message:
    {message}
    """

    # Database operations with error handling
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        email_token, domain = tokenize_email(email)
        TB_NAME = "contact_submissions"  # or use os.getenv("TB_NAME")
        cursor.execute(
            f"""INSERT INTO {TB_NAME} (name, email_token, email_domain, created_on)
            VALUES (%s, %s, %s, CURRENT_DATE)""",
            (name, email_token, domain)
        )
        conn.commit()
    except Exception as e:
        errors["database"] = "Failed to save your submission. Please try again."
        print(f"Database error: {str(e)}")
        return render_template("Contact.html",
            sitekey=os.getenv("hcaptcha-sitekey"),
            errors=errors,
            form_data=request.form)
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

    # Send email with error handling
    try:
        send_email(to_email=email, subject=f"Contact Form: {subject}", body=email_body)
        return render_template("Contact.html",
            success="Thank you! Your message has been sent.",
            sitekey=os.getenv("hcaptcha-sitekey"),
            errors={},
            form_data={'name': '', 'email': '', 'subject': '', 'message': '', 'privacyCheck': False})

    except SMTPRecipientsRefused:
        errors["email"] = "The email address does not exist. Please check and try again."
        return render_template("Contact.html",
            sitekey=os.getenv("hcaptcha-sitekey"),
            errors=errors,
            form_data=request.form)

    except smtplib.SMTPException as e:
        error_msg = str(e)
        if any(code in error_msg for code in ['550', '551', '554']):
            errors["email"] = "The email address was rejected by the server."
        else:
            errors["general"] = "Failed to send email. Please try again later."
        return render_template("Contact.html",
            sitekey=os.getenv("hcaptcha-sitekey"),
            errors=errors,
            form_data=request.form)

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        errors["general"] = "An unexpected error occurred. Please try again."
        return render_template("Contact.html",
            sitekey=os.getenv("hcaptcha-sitekey"),
            errors=errors,
            form_data=request.form)


def tokenize_email(email):
    # Generate a random user ID
    user_id = secrets.randbelow(1000000)  # Generate a random number between 0 and 999,999
    
    # Extract domain from email
    domain = email.split('@')[-1]
    
    # Create the tokenized email in the format User_<random_number>@<domain>
    email_token = f"User_{user_id}"
    
    return email_token, domain

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
