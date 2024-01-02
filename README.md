# Sparks AI

![](./images/DALL-E-Sparks-AI-version-3.png)

## Quick Facts
- **Language:** Python
- **Technologies:**
    - [discord.py](https://github.com/Rapptz/discord.py)
    - [LangChain](https://www.langchain.com/)
    - [OpenAI Assistants](https://platform.openai.com/docs/overview)
- **Database:** Google Cloud Firestore
- **Deployment:** 
    - Containerized with Docker
    - Stored Docker images in Google Artifact Registry
    - Deployed on Google Kubernetes Engine

## Background
Sparks AI is a personal assistant AI designed to assist you with daily tasks, administration, and research. It is still in the early stages of development, so many features are not yet completed. 

## Getting Started

You can run the AI locally by using the included Docker Compose file. To start it, run the following command:
```
docker compose up --build
```

Please note:
- You will need to set up the following API keys in a .env file; see relevant service provider for details:
    - OPENAI_API_KEY
    - DISCORD_TOKEN
    - SERPAPI_API_KEY
- In addition, you will need to set the following environment configurations for Google Cloud:
    - BIGQUERY_TABLE_ID
    - BIGQUERY_USER_DETAILS_TABLE_ID
    - FIREBASE_TABLE_ID
    - GOOGLE_CLOUD_PROJECT
- Finally, initialize the OpenAI assistant configuration by running the `manage.py` file.

## Planned Features

- [ ] Email integration for reading and answering emails
- [ ] Improved internet research capabilities
- [ ] User modeling to predict user requirements for any given task
- [ ] Additional chat channels, including integration with other chat apps and a dedicated web app interface
- [ ] 'Offline' task management for completing tasks asynchronously
- [ ] Improved `manage.py` file for setting up required databases# Sparks AI
