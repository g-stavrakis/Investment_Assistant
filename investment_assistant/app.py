import streamlit as st
import pandas as pd
from assistant import investment_assistant
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv
import os


# Set the page configuration
st.set_page_config(page_title="LLM Investment Assistant", page_icon="🧑‍💻", layout="centered")

# Initialize the selected model to create the embeddings
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

# Read the prepared data
data = pd.read_csv('data/investment_data.csv')
# Explore the first rows of data
companies = sorted(list(data['company'].unique()))

# Custom CSS for a professional feel
st.markdown("""
    <style>
       .main {
            max-width: 85%;  /* This makes the content a bit wider while staying centered */
            margin: 0 auto;
            background-color: #f0f2f6;
        }
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #0D4C92;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)


# Title of the app
st.markdown("<h1 class='title'>🧑‍💻 Your Friendly Investing Assistant</h1>", unsafe_allow_html=True)

# Add an empty line for spacing
st.write("")

# Introduction text
st.markdown("**Welcome to the interactive application powered by your personal LLM Investment Assistant!**")

st.markdown("This nice assistant has thoroughly reviewed the comprehensive 2023 10-K financial reports for over 50 of the most influential companies. Simply select the company you want to explore, ask your question, and let the assistant guide you with insights from the latest reports!")

# Layout: Dropdown and Question Input in separate columns

# Dropdown slider to selected the company to examine
options = companies
selected_company = st.selectbox("Select a company:", options)

# Text input widget for user's question
user_input = st.text_input("Ask the Expert")

# Button to generate response
if st.button("Generate Response", key="generate"):
    if user_input:
        # Create the vector of the query
        vector_query = model.encode(user_input)
        # Simulate LLM model response (replace with actual LLM call)
        response = investment_assistant(user_input,vector_query,selected_company)
        st.success(response)
    else:
        st.error("Please enter a valid question.")

# Provide Feedback
st.markdown("---")

st.markdown("### Provide Your Feedback")
# Thumbs up and Thumbs down buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("👍 Thumbs Up"):
        st.success("Thank you for your positive feedback!")

with col2:
    if st.button("👎 Thumbs Down"):
        st.error("Thank you for your feedback! We'll use this to improve.")

# Footer
st.markdown("---")
st.markdown("*Disclaimer: This app is a project created for the DataTalksClub LLM Zoomcamp. Please don’t rely completely on this assistant for actual financial decisions without verifying the information on your end.*")

