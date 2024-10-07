# Use a lightweight Python image as the base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the Streamlit port  (8502)
EXPOSE 8502


# Run the Streamlit app
CMD ["streamlit", "run", "investment_assistant/app.py", "--server.port=8502"]
