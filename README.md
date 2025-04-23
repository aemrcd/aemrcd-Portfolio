

<h3 style="letter-spacing:5px;"> My Portfolio Website</h3>

### This is my personal portfolio site with a contact form. The form includes spam protection via **hCaptcha** and email validation via **Abstract API**.

## <h3 style="letter-spacing:2px"> 🌐 API Locations </h3> 

- **hCaptcha Endpoint**: This project uses the hCaptcha service to prevent bots. You can find more about it here: [https://www.hcaptcha.com](https://www.hcaptcha.com).
- **Abstract API**: For email validation, the project uses the Abstract API. You can sign up for an API key here: [https://www.abstractapi.com/email-validation](https://www.abstractapi.com/email-validation).

## <h3 style="letter-spacing:2px">  📦 Clone and Setup Project </h3> 

To use the contact form functionality, you’ll need to set up Virtual Environment and the API keys in your `.env` file.

### Steps:
1. Clone the Respository
```bash 
   git clone https://github.com/aemrcd/aemrcd.github.io
```

2. Setup Venv & Activate
- Create a Virtual Environment
```bash
   python -m venv venv
```
- Activate in CMD / Powershell
- #### Powershell
```Powershell
    Venv/Scripts/activate.ps1 
```
- #### CMD
```bash
    Venv/Scripts/activate.bat 
```
3.Install Requirements
```bash
    pip install -r requirements.txt
```

### Creating ".env"  getting the api keys:
1. Create a `.env` file in the root of the project.
2. Add the following environment variables:
   ```plaintext
   HCAPTCHA_SECRET_KEY=your_hcaptcha_secret_key
   ABSTRACT_API_KEY=your_abstract_api_key
