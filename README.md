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
- Put the .env file in the same folder where the docker-compose file is located
- Run docker compose up -d (-d : the container will run in the background. You will not able to see the logs)
- Optional : Run this command in the terminal for testing purpose (docker compose exec db_pgvector psql -U takos -d ragdb -h db_pgvector)

## 2 -  Start building basic rag pipeline
- uv run python -m production_rag_system.ingest --path data/docs/restaurant.pdf --reset : this command allow me to process the pdf data and store inside pgvector.
- Run this to ask a question : uv run python -m production_rag_system.query --q "Le Burger Gourmet contient-il du gluten ?"  
