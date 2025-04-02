import re  
import requests  
from flask import Flask, render_template, request, jsonify  
import json  
import os 
from dotenv import load_dotenv 

app = Flask(__name__)


load_dotenv()
HCAPTCHA_SECRET_KEY = os.getenv("HCAPTCHA_SECRET_KEY")
valid_email_file = "email_list.json"

# Load valid domains from the JSON file
def load_valid_emails(valid_email_file):
    try:
        with open(valid_email_file, 'r') as file:
            emails = json.load(file)
            return set(emails.get("valid_domains", []))  # This will find the valid mails in a json file
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
    form_data = request.get_json()
    captcha_token = form_data.get('captcha')
    email = form_data.get('email')

    print("Loaded emails:", VALID_EMAILS)  
    print("Checking email:", email)  

    if not captcha_token:
        return jsonify({"success": False, "message": "No Captcha Token Provided"})

    verification_response = verify_captcha(captcha_token)

    if not verification_response['success']:
        return jsonify({"success": False, "message": "Captcha Verification Failed"})

    if not is_email_format_valid(email):
        return jsonify({"success": False, "message": "Invalid email format"})

    if not is_valid_email(email):
        return jsonify({"success": False, "message": "Email is not valid"})

    return jsonify({"success": True, "message": "Form submitted successfully"})

# Verify captcha
def verify_captcha(captcha_token):
    url = 'https://hcaptcha.com/siteverify'  
    data = {'secret': HCAPTCHA_SECRET_KEY, 'response': captcha_token}
    response = requests.post(url, data=data)  
    return response.json()  



@app.route('/Contact')
def Contact():
    sitekey = os.getenv("hcaptcha-sitekey") 
    return render_template("Contact.html", sitekey=sitekey)

@app.route('/Home')
def Home():
    return render_template("Index.html")

if __name__ == '__main__':
    app.run(debug=True)  
