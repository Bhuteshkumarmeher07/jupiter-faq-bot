# Dockerfile for Hugging Face Space using FAISS + Streamlit
FROM python:3.10-slim

# Avoid prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port and run Streamlit
CMD streamlit run app.py --server.port 7860 --server.address 0.0.0.0 --server.enableCORS false
