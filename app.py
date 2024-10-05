import streamlit as st
import pandas as pd

# Read the prepared data
data = pd.read_csv('data/investment_data.csv')
# Explore the first rows of data
companies = sorted(list(data['company'].unique()))

# Title of the app
st.title("Your Friendly Investing Advisor")

# Dropdown slider to selected the company to examine
options = companies
selected_option = st.selectbox("Select a company:", options)

# Text input widget for user's question
user_input = st.text_input("Ask the Exprert")

# Button to generate response
if st.button("Generate Response"):
    # Simulate LLM model response (replace with actual LLM call)
    response = f"Generated response for your question: '{user_input}' with {selected_option}"
    st.write(response)

# Thumbs up and Thumbs down buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("👍 Thumbs Up"):
        st.write("You gave a thumbs up!")

with col2:
    if st.button("👎 Thumbs Down"):
        st.write("You gave a thumbs down!")

