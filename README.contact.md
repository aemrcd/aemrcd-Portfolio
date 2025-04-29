

## **<h3 style="letter-spacing:2px"> 🌐 API Locations </h3>**


## **hCaptcha Endpoint**: This project uses the hCaptcha service to prevent bots. You can find more about it here: [https://www.hcaptcha.com](https://www.hcaptcha.com).

### How to Get Your hCaptcha Site Key & Secret Key  <img src="https://wpforms.com/wp-content/uploads/2024/09/hcaptcha-logo.png" width="40" height="40">


Follow these steps to set up hCaptcha and integrate it into your project:

1. **Go to the hCaptcha website:**  
   👉 [https://www.hcaptcha.com](https://www.hcaptcha.com)

2. **Sign up or log in** to your account.

3. In the dashboard, navigate to the **“Sites”** tab.

4. Click **“New Site”** to register your domain.
   - For local development, you can use `localhost` as the domain.

5. Under the **General Info** section:
   - Enter your **site domain** (`example.com` or `localhost`).
   - (Optional) Set your **difficulty level** for the CAPTCHA challenge.

7. After saving your site, hCaptcha will provide you with:
   - ✅ **Site Key** – used in your frontend ([Contact](templates/Contact.html)) this is in Dashboard 
   - 🔒 **Secret Key** – used in your backend (Flask) this is normally on the settings

8. Add these keys to your `.env` file:
   - ***⚠️ MAKE SURE TO PLACE ALL KEYS IN `.env`⚠️***
   ```
   HCAPTCHA_SECRET_KEY=your_site_key_here
   SECRET_KEY=your_secret_key_here
   ```
   
## **Abstract API**: For email validation, the project uses the Abstract API. You can sign up for an API key here: [https://www.abstractapi.com/email-validation](https://www.abstractapi.com/email-validation).

## 📧 How to Set Up Abstract API for Email Validation (Python + Flask)

This Flask project uses the **Abstract API Email Validation** service to verify that email addresses submitted through the contact form are **valid, deliverable**, and **not disposable**.

### 🔧 Steps to Get Your Abstract API Key

1. **Go to the Abstract API website**  
   👉 [https://www.abstractapi.com/email-validation](https://www.abstractapi.com/email-validation)

2. **Create an account** (or log in if you already have one).

3. Navigate to the **Email Validation API** section in the dashboard.

4. Click **“Get Started”** to create a new application.

5. After setup, you'll see your **API Key**. Copy it.

--- 

### Creating ".env"  getting the api keys:
1. Create a `.env` file on the main branch of the project.
2. Add the following environment variables:
   ```plaintext
   HCAPTCHA_SECRET_KEY=your_hcaptcha_secret_key
   ABSTRACT_API_KEY=your_abstract_api_key

3. Use `python-doten` to load them into your Flask app securely.

<img src="User-Manual-img/Flowchart.gif" style="border-radius: 10px; border: 1px solid #000; width: 760px; height: 400px; ">
