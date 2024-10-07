# Importing necessary libraries
import pandas as pd
from elasticsearch import Elasticsearch
from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .envrc for the Chat GPT
load_dotenv("../.envrc")

# Initialize the openai instance
client = OpenAI()

# Create the hybrid search function for information retrieval
def document_search(query, vector, company, a = 0.75):
    # This is the query for the vector search with the best field 
    vector_query = {
        "field": 'question_answer_context_vector',
        "query_vector": vector, # This will recieve a vector of the user query
        "k": 5,
        "num_candidates": 10000,
        "boost": a, # Here you can set up the weight the vector search will have in the results
        "filter": {
            "term": {
                "company": company
            }
        }
    }
    # This is the query for the keyword search with best boosting
    keyword_query = {
        "bool": {
            "must": {
                "multi_match": {
                    "query": query, # This will recieve the user query itself
                    "fields": ["question", "answer", "context"],
                    "type": "best_fields",
                    "boost": 1-a, # Here you can set up the weight the keyword search will have in the results
                }
            },
            "filter": {
                "term": {
                    "company": company
                }
            }
        }
    }
    # Here is the combination of the two search methods
    search_query = {
        "knn": vector_query,
        "query": keyword_query,
        "size": 5,   # This is the number of the returned documents
        "_source": ['question', 'answer', 'context', 'ticker' ,'company' ,'id'] # The fields that will be returned for each retrieved document 
    }

    es_results = es_client.search(
        index=index_name,
        body=search_query
    )
    
    result_docs = []
    
    for hit in es_results['hits']['hits']:
        result_docs.append(hit['_source'])

    return result_docs



# Create the function will generate the context
def context_generation(retrieved_docs):
    # Initialize context
    context = ''
    # Create context for each document
    for record in retrieved_docs:
        context += 'question: {question} answer: {answer} \n\n'.format(**record)
    # Return context
    return context

# Create the prompt template
prompt_template = '''
You are an Investment Assistant with deep expertise in financial markets.
Provide a fact-based answer to the user's QUESTION strictly using the information provided in the CONTEXT. 
Do not include opinions or external knowledge.

QUESTION: {question}

CONTEXT: 
{context}
'''.strip()

# Create a function to create the prompt
def prompt_generation(query, retrieved_docs, prompt_template = prompt_template):
    # Create the context
    prompt_context = {}
    prompt_context['question'] = query
    prompt_context['context'] = context_generation(retrieved_docs)
    # Generate the prompt
    prompt = prompt_template.format(**prompt_context)
    return prompt

# Create the function to request an answer from an LLM
def ask_llm(prompt, model='gpt-3.5-turbo'):
    # Create the request body and make the request
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


# Create the RAG function combining all the above information
def investment_assistant(query, vector, company ,prompt_template = prompt_template):
    # Retrieve the relevant documents
    relevant_docs = document_search(query,vector,company)
    # Create the prompt for the model
    prompt = prompt_generation(query, relevant_docs, prompt_template = prompt_template)
    # Ask the LLM model
    response = ask_llm(prompt)
    return response