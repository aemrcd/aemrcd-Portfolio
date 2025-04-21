import smtplib
from flask import Flask, render_template, request
import os
import requests
from dotenv import load_dotenv
from SMTP import send_email
from smtplib import SMTPRecipientsRefused
import json
import hashlib


# # Test script
# from SMTP import send_email

# try:
#     send_email(
#         to_email="recipient@example.com",
#         subject="Test Email",
#         body="This is a test email"
#     )
#     print("Test successful!")
# except Exception as e:
#     print(f"Test failed: {str(e)}")



## TESST FOR EMAIL MASKING
# def unspecified_email(email):
#     username, domain = email.split('@')
#     if len(username) >= 2:
#         masked = username[:2] + '*' * (len(username) - 2)
#     else:
#         masked = '*' * len(username)
#     return masked, domain

# # Test it
# email = "aeshan@gmail.com"
# masked_email, domain = unspecified_email(email)

# print("Masked Email:", masked_email)
# print("Domain:", domain)




# Function to convert email into a token
def tokenize_email(email):
    try:
        # Split the email to get the domain (everything after @)
        domain = email.split('@')[-1]

        # Hash the email to get a unique, fixed-size string
        email_hash = hashlib.sha256(email.encode()).hexdigest()

        # Take the hash and convert it to a number within a 5-digit range
        token_number = int(email_hash, 16) % 100000

        # Create a "tokenized" version of the email in this format: User_XXXXX@domain
        tokenized_email = f"User_{token_number}@{domain}"

        return tokenized_email, domain

    except Exception as e:
        # If an error occurs, print the error and return None
        print(f"Error: {e}")
        return None, None

# Main part that runs when executing the script
if __name__ == "__main__":
    # Test email to process
    email = "aerolmercado09@gmail.com"

    # Call the function to tokenize the email
    tokenized_email, domain = tokenize_email(email)

    # Print the results if the tokenization was successful
    if tokenized_email:
        print(f"Original Email: {email}")
        print(f"Tokenized Email: {tokenized_email}")
        print(f"Domain: {domain}")
    else:
        print("Failed to tokenize the email.")
