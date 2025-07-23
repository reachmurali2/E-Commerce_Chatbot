🛍️ E-Commerce Chatbot — Brief Overview
The E-Commerce Chatbot is an intelligent conversational assistant designed to enhance the shopping experience by answering customer queries and helping users discover products using natural language. Built using Generative AI, Semantic Routing, and Vector Databases, it mimics a real customer support agent with capabilities far beyond basic keyword matching.

🔍 What It Can Do:
Understand and respond to frequently asked questions (FAQs) like return policy, delivery time, payment modes, etc.

Perform natural language search over the product database (e.g., "Show top 3 Nike shoes under ₹3000").

Dynamically route queries: Uses AI to determine if the user query is a FAQ or a data-driven SQL search.

Retrieve answers using RAG (Retrieval-Augmented Generation) from vector databases (ChromaDB) for unstructured data.

Auto-generate SQL queries and summarize tabular data using LLM for structured product queries.

Built with a simple and interactive Streamlit UI for chatting in real time.

This chatbot combines the power of LLMs, semantic understanding, and backend data intelligence to serve as a smart AI assistant for any e-commerce platform.



🛍️ E-Commerce Chatbot using LLM, RAG & Vector Search
🔎 Overview
This is an intelligent e-commerce chatbot app built using:

LangChain for chaining logic

Groq (LLM) for answer generation

ChromaDB as a vector store for semantic search

Semantic Router for intelligent routing of user queries

Streamlit for the interactive frontend

SQLite for structured product data queries

Selenium for Flipkart product scraping

The chatbot can:

Answer FAQs about orders, returns, payments, delivery, etc.

Search the product catalog using natural language

Generate SQL queries to fetch and summarize product data

Combine structured + unstructured RAG (Retrieval-Augmented Generation)

📦 Features
✅ FAQ Chat: Understands and responds to general customer queries
✅ SQL Product Search: Converts queries like "Nike shoes under ₹3000" into SQL
✅ Semantic Router: Determines whether the query is FAQ or product-related
✅ ChromaDB Integration: Finds relevant knowledge using embeddings
✅ Groq LLM: Generates context-aware answers using llama-3.3-70b-versatile
✅ Streamlit UI: Intuitive chat interface with real-time conversations
✅ Web Scraping: Automated Flipkart product scraping & storage in SQLite
✅ RAG Design: Combines vector + SQL data for grounded answers

🏗️ Project Structure
graphql
Copy
Edit
ecommerce-chatbot/
│
├── streamlit_app.py                # Main Streamlit UI app
├── faq.py                          # FAQ ingestion, vector search, and answer generation
├── sql.py                          # SQL generation, query execution, and response generation
├── router.py                       # Semantic router for query type detection
├── data_extractor.py              # Flipkart product details scraping
├── product_scraper.py             # Flipkart listing page scraper
├── db_loader.py                   # Loads product CSV into SQLite DB
├── resources/
│   └── faq_data.csv                # FAQ questions and answers
├── db.sqlite                       # SQLite database for product data
├── flipkart_product_data.csv       # Scraped product data
├── requirements.txt                # Python dependencies
└── README.md                       # You're reading it!
🚀 Getting Started
🔧 Installation
bash
Copy
Edit
git clone https://github.com/your-username/ecommerce-chatbot.git
cd ecommerce-chatbot
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate on Windows
pip install -r requirements.txt
🌍 Set Environment Variables
Create a .env file:

ini
Copy
Edit
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
💻 Usage
1. Scrape Flipkart Products
bash
Copy
Edit
python data_extractor.py         # or product_scraper.py
python db_loader.py              # loads into SQLite
2. Run Streamlit App
bash
Copy
Edit
streamlit run streamlit_app.py
✨ Sample Queries
FAQ:

How can I track my order?
What is the refund policy?

SQL Search:

Show all Puma shoes under ₹3000
List 3 best-rated Nike running shoes

🧠 Tech Stack
Tech	Purpose
Streamlit	Web app frontend
LangChain	LLM chaining & prompt logic
Groq	LLM for response generation
ChromaDB	Vector database (RAG)
Semantic Router	Query type classification
SQLite	Structured product DB
Selenium	Flipkart product scraping

🧩 Future Improvements
Add memory for conversation history

Integrate user login & chat history

Use advanced embedding models like text-embedding-3-large

Deploy on Streamlit Cloud or AWS EC2

📸 UI Preview
<img src="streamlit_app_demo.gif" width="100%" alt="Chatbot Demo UI" />
📄 License
MIT License. Free for personal and commercial use.