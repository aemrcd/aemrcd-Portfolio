
## API Guide

## <h3 style="letter-spacing:2px"> 🌐 API Locations </h3>

- **hCaptcha Endpoint**: This project uses the hCaptcha service to prevent bots. You can find more about it here: [https://www.hcaptcha.com](https://www.hcaptcha.com).
- **Abstract API**: For email validation, the project uses the Abstract API. You can sign up for an API key here: [https://www.abstractapi.com/email-validation](https://www.abstractapi.com/email-validation).






### Creating ".env"  getting the api keys:
1. Create a `.env` file in the root of the project.
2. Add the following environment variables:
   ```plaintext
   HCAPTCHA_SECRET_KEY=your_hcaptcha_secret_key
   ABSTRACT_API_KEY=your_abstract_api_key

3. Use `python-doten` to load them into your Flask app securely.
<img src="User-Manual-img/Flowchart.gif" style="border-radius: 10px; border: 1px solid #000; width: 760px; height: 400px; ">
