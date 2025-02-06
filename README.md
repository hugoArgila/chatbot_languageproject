# Chatbot using Azure Language Service

## Local Contents
- **qna-app.py**: python code that contains the main Flask code y the logic to call the Language Service API from Azure.
- **templates/index.html**: HTML template that contains the chatbot interface
- **.env**: secret archive with the environment variables to connect to our API(AI_SERVICE_ENDPOINT, AI_SERVICE_KEY, QA_PROJECT_NAME, QA_DEPLOYMENT_NAME).

## Online Contents
- **qna-app.py**: python code that contains the main Streamlit code y the logic to call the Language Service API from Azure.
- **.env**: secret archive with the environment variables to connect to our API(AI_SERVICE_ENDPOINT, AI_SERVICE_KEY, QA_PROJECT_NAME, QA_DEPLOYMENT_NAME).

## Chatbot Local Deployment

### Step 1: Dependencies installation
First, make sure you have installed the libraries in the [requirements.txt](https://github.com/hugoArgila/chatbot_languageproject/blob/main/mi_chatbot_app/requirements.txt) archive. If not install them in your terminal using the pip command.

### Step 3: Configure your .env
You will need to configure a .env with the enviroment variables to connect to our Azure API.

### Step 3: Run Python Code
Next, you will have to run your python code in your terminal using the command:
```bash
python qna-app.py
```

 ### Step 4: Enter your App 
 Finally, you will have to enter inside a web browser to your app using this link: **http://127.0.0.1:5000/**

 ## Conversation Analysis

 ### Entities
- Awards
- Cities
- GameDates
- GameScores
- Players
- Positions
- Stadiums
- Stats
- Teams

### Intents
- GetAwards
- GetCity
- GetGameDates
- GetPlayer
- GetPosition
- GetStadium
- GetStats
- GetTeam

### Utterance Examples for testing
- Tell me about Michael Jordan
- Who holds the record for most assists in NBA history?
- How many championships does LeBron James have?
- Where does the lakers play?
- Which city is home to the Houston Rockets?
- When did the Chicago Bulls win their first NBA championship?
- What was the score of Kobe Bryant’s 81-point game?


