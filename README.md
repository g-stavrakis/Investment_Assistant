# Investment Assistant


# Problem Description

Investors and traders often face challenges when analyzing 10-K reports from large companies due to their length and complexity. These reports are packed with detailed financial statements, risk disclosures, management discussion and analysis (MD&A), making it difficult to quickly extract relevant insights. For casual investors, understanding financial jargon and metrics can be overwhelming, while experienced investors struggle with the time-consuming process of analyzing multiple reports. The critical information, such as key risks or growth opportunities, is often buried deep within the documents, and the need to act fast on new data makes the process even more daunting.

# Investor Assistant

The Investment Assistant is an LLM-powered QA RAG system that breaks 2023 10-K financial reports from 60+ large companies into meaningful chunks, addresses these challenges by allowing users to interact with the reports in real time. This enables quick retrieval of key insights, simplifies complex financial data, and provides accurate, context-aware responses to specific queries. By offering immediate access to critical financial information, risks, and opportunities, the tool empowers investors to make informed decisions and act swiftly on newly released data, staying ahead of market movements.

# Technology Stack

- Python 3.9
- Streamlit: For the Application
- Elasticsearch: For hybrid Search
- OpenAI: For the LLM 

# Dataset

# Code

# Running the Application
To run the application you need to follow the below steps:

1. Install the dependencies for the project
```bash
pip intall requirements.txt
```
2. Set up your openAI API key into an environmental variable

Copy .envrc_template into .envrc and insert your key there. - the .envrc will be picked up by the .gitignore file

3. Run the docker-compose file to initialize all the services used in the application - such as elastic search
```bash
docker-compose up --build
```
4. Then connect to the application's folder
```bash
cd investment_assistant
```
5. Run this command to fetch all files in the elastic search index
```bash
python db_prep.py
```
6. Run the streamlit application
```bash
streamlit run app.py
```
7. Access the application from http://localhost:8501

