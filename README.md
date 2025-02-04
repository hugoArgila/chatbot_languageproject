# Chatbot using Azure Language Service

## Contents
- **qna-app.py**: python code that contains the main Flask code y the logic to call the Language Service API from Azure.
- **templates/index.html**: HTML template that contains the chatbot interface
- **.env**: secret archive with the environment variables to connect to our API(AI_SERVICE_ENDPOINT, AI_SERVICE_KEY, QA_PROJECT_NAME, QA_DEPLOYMENT_NAME).
  
## Chatbot Local Deployment

### Step 1: Dependencies installation
First, make sure you have installed the libraries in the [requirements.txt](https://github.com/hugoArgila/chatbot_languageproject/blob/main/mi_chatbot_app/requirements.txt) archive. If not install them in your terminal using the pip command.

### Step 2: Run Python Code
Next, you will have to run your python code in your terminal using the command:
```bash
python qna-app.py
```

 ### Step 3: Enter your App 
 Finally, you will have to enter inside a web browser to your app using this link: **http://127.0.0.1:5000/**
