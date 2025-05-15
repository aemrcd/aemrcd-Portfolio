
<h1 style="letter-spacing:5px; font-style:=bold;"> My Portfolio Website</h1>

#### This is my personal portfolio site with a contact form. The form includes spam protection via **hCaptcha** and email validation via **Abstract API**.

# **📚 Table of Contents**

### 1. [Clone and Setup Project](README.md#-clone-and-setup-project-)
### 2. [Database Setup](README.md#%EF%B8%8F-database-setup)
### 3. [API Locations](README.md#-api-locations)
   - [hCaptcha Setup](README.md#hcaptcha-endpoint-this-project-uses-the-hcaptcha-service-to-prevent-bots-you-can-find-more-about-it-here-httpswwwhcaptchacom)
   - [Abstract API Setup](README.md#abstract-api-for-email-validation-the-project-uses-the-abstract-api-you-can-sign-up-for-an-api-key-here-httpswwwabstractapicomemail-validation)
### 4. [Website Features](README.md#%EF%B8%8F-website-features)

#  📦 Clone and Setup Project </h2> 

#### To use the contact form functionality, you’ll need to set up Virtual Environment and the API keys in your `.env` file.

#### Follow these simple steps to clone the repository to your local machine:

1. **Create a folder** where you want to store the cloned files:

   - You can create a folder anywhere on your computer (example, in your "Documents" or on your desktop).

2. **Open the Command Prompt**:
   
   - Press `Windows Key + R` to open the "Run" menu.
   - Type `cmd` and press **Enter**. This will open the Command Prompt.

3. **Clone the Repository**
   
   - In the Command Prompt, use the `git clone` command to clone the repository into the folder you created:

   ```bash
    git clone https://github.com/aemrcd/aemrcd.github.io
   ```
   
   - Installing libraries to python by typing the following commands. This will download all the libraries to use the website.

    ```bash 
    pip install -r requirements.txt
    ```
    
4. **Setup Venv & Activate**:
   - Create a Virtual Environment
     
   ```bash
      python -m venv venv
   ```
   
   - Powershell Activate in Powershell
   ```Powershell
      .\venv\Scripts\activate     
   ```

# 🗃️ Database Setup 

## 1. Installing MariaDB to PI/Virtual Machine
### Make sure you install Ubuntu on your `PI` & `Virtual Machine`

- Press `Windows Key` to open the "Search" menu.
   - Type `Terminal` and press **Enter**. This will open the Terminal Prompt.
   - install MariaDB by typing: 
```bash 
    sudo apt install mariadb-server
```
```bash
    sudo mariadb_secure_installation
```
## 2. Creating and Managing Databases
 1. Log in to MariaDB as root:

```bash
    sudo mysql -u root -p
```
 2. Create a new database:
```bash
    CREATE DATABASE my_database;
```
 3. Create a new user and grant privileges:
```bash
    CREATE USER 'my_user'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON my_database.* TO 'my_user'@'localhost';
    FLUSH PRIVILEGES;
```
 4. Exit MariaDB:
```bash
    EXIT;
```
## 3. Managing Tables in MariaDB:

1. Showing The Database:
- This statement works to show all of your database.
```bash
   SHOW DATABASES;
```
2. SELECTING The Database:
- This statement works if you have multiple database.
```bash
   USE "yourdatabase";
```
3. Viewing tables in your database
- To see the data inside a table, use the `SELECT` query. Replace `"yourtable"` with the name of the your table  to view.

```bash
   SELECT * FROM "yourdatabase";
```
4. Deleting a Row from a Table

- If you want to delete a specific row in a table, use the   `DELETE` statement with a `WHERE` and  Replace `"yourtable"` with the your table name and `"PLACE_YOUR_ID"` with the ID or condition to delete a spesific row.

```bash
    SELECT * FROM  "yourdatabase" WHERE Id IN = "PLACE_YOUR_ID";
```



#  🌐 API LOCATIONS 

<details>
<summary style="font-weight: bold; font-size: 15px;">Api Tutorial</summary>

### Creating ".env"  getting the api keys:
1. Create a `.env` file on the main branch of the project.
2. Add the following environment variables:
   ```plaintext
   HCAPTCHA_SECRET_KEY=your_hcaptcha_secret_key
   SECRET_KEY=your_secret_key
   ABSTRACT_API_KEY=your_abstract_api_key
   ```
   
3. Use `python-doten` to load them into your Flask app securely.

--- 

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

</details>

#  🖥️ WEBSITE FEATURES 

<details>
<summary>🖥️ WEBSITE FEATURES</summary>

<div align="center" >

### **Flowchart:**  
<img src="static/PICTURE/Flowchart.gif" alt="Flowchart" width="400px" style="border-radius: 12px;">

### **Modern Web Design Preview:**  
<img src="static/PICTURE/Web-main.gif" alt="Web Design" width="400px" style="border-radius: 12px;">

</div>

