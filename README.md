# production_rag_system
The goal is to explore all the steps to build a production rag system 


## 1 -  Project setup using UV 
- Ouvre le folder 
- Setup venv : uv venv --> source .venv/bin/activate
- Select interpreter : CTRL + SHIFT + P
- Execute : 'uv init --package .' This will initiate the package and allow me to create a separate folder to test my project.
- create requirements.txt file and add package name
- Install package from requirements.txt : uv add -r requirements.txt
- If you want to install a specific package run : uv add packagename
- Create .env file to store keys
- Populate information inside the docker-compose.yml
- Create the folder inside data for the volume. I will not commit those file
- Run docker compose up -d (-d : the container will run in the background. You will not able to see the logs)

## 2 -  Start building basic rag pipeline
