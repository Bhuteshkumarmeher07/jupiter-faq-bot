Jupiter Help Center FAQ Bot 🤖

This project is a smart AI-powered FAQ assistant built as a submission for the AI Internship assignment by Jupiter. It simulates a real-world customer support bot for banking, capable of understanding natural language queries, retrieving the most relevant help articles, and rephrasing answers in a friendly, professional tone.

🔍 Problem Statement

The goal is to build a conversational assistant that can:

Search and retrieve the most relevant FAQ from Jupiter's public community help portal.

Rephrase that answer in a human-like, helpful tone.

Handle queries in English, Hindi, or Hinglish.

Track usage and allow user feedback for continuous improvement.

🚀 Features

✅ Core Functionalities

Semantic FAQ Retrieval: Uses sentence-transformers with FAISS vector store to semantically match user questions with Jupiter FAQs.

LLM Rephrasing: Uses the mistralai/mistral-small-3.2-24b-instruct-2506:free model via OpenRouter API to rewrite answers clearly and politely.

Multilingual Support: Automatically detects Hindi or Hinglish inputs and translates them to English before processing.

Token Usage Tracking: Displays prompt, completion, and total token usage for every OpenRouter call.

Feedback Collection: Allows users to rate answers (👍 / 👎) and submit comments for further improvement.

🎁 Bonus

Works entirely in-browser using Streamlit.

Caches last result to prevent content loss when interacting with buttons.

🖼️ Sample UI (Demo Preview)
![Jupiter FAQ Bot UI](demo_faq.png)


🖥️ Run Locally

1. Clone the Repo

git clone https://github.com/your-username/jupiter-faq-bot.git
cd jupiter-faq-bot

2. Install Dependencies

pip install -r requirements.txt

3. Run the App

streamlit run app.py

🧠 Technologies Used

Python 3.10+

Streamlit — for the frontend UI

FAISS — for fast vector similarity search

Sentence-Transformers — for embeddings (all-MiniLM-L6-v2)

OpenRouter API — for free access to Mistral LLM

langdetect + googletrans — for multilingual input support

📁 Folder Structure

├── app.py                      # Streamlit main app
├── rephrase_with_mistral.py   # LLM interaction
├── semantic_search.py         # Embedding + vector search
├── cleaned_faqs.json          # Jupiter help data (scraped + cleaned)
├── feedback_log.csv           # User feedback (optional)
├── requirements.txt           # All dependencies
└── README.md                  # Project overview

📦 Requirements

streamlit
sentence-transformers
faiss-cpu
openai
langdetect
googletrans==4.0.0-rc1

📤 Deployment (Optional)

You can deploy this app on:

Streamlit Cloud: https://streamlit.io/cloud

Hugging Face Spaces (Gradio or Streamlit template)

Just connect your GitHub repo and set the entry point to app.py.

📫 Submission Guide (for Jupiter)

When sharing the project:

Include this GitHub repository link

Optionally, include a live demo link via Streamlit Cloud

Mention tech used + highlight Hindi/Hinglish input and token tracking support

👨‍💻 Developed By

Your NameAI Intern Applicant @ Jupiter

Feel free to reach out if you'd like to collaborate, improve this bot, or need help deploying it!
