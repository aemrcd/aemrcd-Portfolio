# 🚀 Deploying Your Flask App to Azure with GitHub Actions - A Student-Friendly Guide


### These steps guide you through deploying your Flask web app to Azure using the Azure Web App service.


## What You'll Need:

* An Azure account ([Sign up here](https://azure.microsoft.com/))
* Azure CLI installed ([Download it here](https://docs.microsoft.com/cli/azure/install-azure-cli))
* A Flask app pushed to GitHub

---

## 🌟 Let's Get Started!

### 1. Create a Resource Group

Think of a resource group as a digital folder where you keep all the stuff related to your app. To make one, open your terminal and run:

```powershell
az group create --name myResourceGroup --location eastus
```

---

### 2. Set Up Your App Service Plan

An App Service Plan is basically where you decide how much power (like CPU and RAM) your app gets. Run this:

```powershell
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux
```

---

### 3. Create the Web App

Now, let's actually set up the web app on Azure:

```powershell
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myFlaskApp --runtime "PYTHON|3.8"
```

---
### 4. Connect GitHub and Set Up Deployment

1. **Open Azure Portal:**  
    Go to [portal.azure.com](https://portal.azure.com/) and select your Web App.

2. **Go to Deployment Center:**  
    In your Web App's menu, click **Deployment Center**.

3. **Connect to GitHub:**  
    - Choose **GitHub** as the source.
    - Sign in if needed.
    - Pick your repository and branch (usually `main`).

4. **Select Build Provider:**  
    - Choose **GitHub Actions**.
    - Review the suggested workflow file.

5. **Finish Setup:**  
    - Click **Save** or **Finish**.
    - Azure adds a workflow file to `.github/workflows/` in your repo.

6. **(Optional) Use a Custom Workflow:**  
    - Replace the generated file with your own (see example below).
    - Commit it to `.github/workflows/azure-webapp.yml`.

Now, whenever you push changes to your branch, Azure will automatically deploy your app for you. 

---

### 📦 GitHub Actions Workflow

Create a new file at `.github/workflows/azure-webapp.yml` and paste this:

```yaml
name: Deploy Flask App to Azure

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Grab the Code
      uses: actions/checkout@v3

    - name: Set Up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'

    - name: Install Libraries
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Deploy to Azure
      uses: azure/webapps-deploy@v2
      with:
        app-name: ${{ secrets.AZURE_WEBAPP_NAME }}
        slot-name: 'production'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
        startup-command: 'gunicorn --bind 0.0.0.0:8000 app:app'
```

---

### 5. Flask App Setup

In your project, make sure `requirements.txt` includes:

```
Flask==2.0.1
gunicorn==20.1.0
```

Your `app.py` file should look like this:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Azure!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

---

### 6. Environment Variables

To set environment variables for your app:

1. Go to the [Azure Portal](https://portal.azure.com/) and find your Web App.
2. In the left menu, under **Settings**, select **Configuration**.
3. Click **+ New application setting** for each variable (example, `SECRET_KEY`, `DATABASE_URL`).
4. Enter the name and value, then click **OK**.
5. After adding all variables (from your `.env` file), click **Save** to apply changes.

Azure uses these settings to securely store secrets like passwords or API keys, so your app can access them without exposing them publicly.


---

### 7. Monitor the Web app

**Monitor Your App with Log Stream:**

1. Go to the [Azure Portal](https://portal.azure.com/) and select your Web App.
2. In the left menu, under **Monitoring**, click **Log stream**.
3. Click **Start** to view real-time logs from your app (requests, errors, etc.).
4. Use these logs to debug issues or check app activity.


---

### 8. Test Your Live App

After the deployment finishes, go to:

```
https://<your-app-name>.azurewebsites.net
```

Any changes you push to GitHub will automatically update your Web app. 
