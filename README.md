# Sparks AI

![](./images/DALL-E-Sparks-AI-version-3.png)

## Quick Facts
- **Language:** Python
- **Technologies:**
    - [discord.py](https://github.com/Rapptz/discord.py)
    - [LangChain](https://www.langchain.com/)
    - [Open AI Assistants](https://platform.openai.com/docs/overview)
- **Database:** Google Cloud Firestore
- **Deployment:** 
    - Containerised with Docker
    - Stored Docker images on Google Artifact Registry
    - Deployed on Google Kubernetes Engine

## Background
Sparks AI is a personal assistant AI designed to assist you with daily tasks, administration and research. It is still in the early stages of development, so many features are not yet completed. 

## Getting Started

You can run the AI locally yourself by using the included Docker compose file. To start it run the following command:
```
docker compose up --build
```

Please note:
- You will need to set up the following API keys in a .env file.
    - OPENAI_API_KEY
    - DISCORD_TOKEN
    - SERPAPI_API_KEY
        - These keys will need to be set up with each relevent service provider
 - In addition, you will need to set the following environment configurations for Google Cloud
    - BIGQUERY_TABLE_ID
    - BIGQUERY_USER_DETAILS_TABLE_ID
    - FIREBASE_TABLE_ID
    - GOOGLE_CLOUD_PROJECT

## Planned Features

- [ ] Email integration to read and answer emails
- [ ] Improved internet research capabilities
- [ ] User modelling to predict user requirements for any given tasks
- [ ] Additional chat channels, including other chat apps and dedicated web app interface
- [ ] 'Offline' task management to allow completing tasks asynchronously