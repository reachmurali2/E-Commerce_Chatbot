# 📦 1. Imports and Setup
import os                                                                                                          # Allows access to OS-level environment variables like API keys. / Access environment variables like API keys.                     
from pathlib import Path                                                                                           # OS-independent file path handling.
import chromadb                                                                                                    # Client for vector store.
from chromadb.utils import embedding_functions                                                                     # To embed text using sentence transformers. 
from groq import Groq                                                                                              # Chat LLM clinet for generating answers.
import pandas as pd                                                                                                # Reading FAQ data from csv file. 
from dotenv import load_dotenv                                                                                     # Loads .env file to access secrets locally.

# 🔐 2. API Key & Embedding Function
load_dotenv()                                                                                                      # Loads .env file into environment variables.
api_key = os.getenv("GROQ_API_KEY")                                                                                # Fetches your GROQ API KEY 
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='sentence-transformers/all-MiniLM-L6-v2') # Sentence transformer embedding model to convert questions into vector form

# 📂 3. Initialize Paths and Clients
faqs_path = Path(__file__).parent/"resources/faq_data.csv"                                                         # Path to the FAQ CSV File.
chroma_client = chromadb.Client()                                                                                  # ChromaDB client to manage collections.
groq_client = Groq(api_key=api_key)                                                                                # LLM client for generating responses.
collection_name_faq = 'faq'                                                                                        # Name of the vector collection for sorting FAQs

# 🧠 4. Ingest FAQ Data 
def ingest_faq_data(path):                                                                                         # Reads the CSV, converts questions to embeddings, and stores them in ChromaDB if not already present.
    if collection_name_faq not in [collection_name for collection_name in chroma_client.list_collections()]:         
        print("Ingesting FAQ data into Chromadb...")     
        collection = chroma_client.get_or_create_collection(name=collection_name_faq, embedding_function=ef)       # function behaves similarly like get_collection, but will create the collection if it doesn't exist.
        df = pd.read_csv(path)                                                                                     # Reads the FAQ file into a DataFrame.
        docs = df['question'].to_list()                                                                            # Extracts all questions. 
        metadata = [{'answer':ans} for ans in df['answer'].to_list()]                                              # stores answers in a dictionary for each question.
        ids = [f"id_{i}" for i in range(len(docs))]                                                                # Generates uqiue IDs for each document.
        collection.add(documents=docs, metadatas=metadata, ids=ids)                                                # Adds documents to Chroma vector DB
        print(f"FAQ Data successfully ingested into chroma collection: {collection_name_faq}")
    else:
        print(f"Collection: {collection_name_faq} already exist")

# 🔍 5. Get Relevant Questions                                                                              
def get_relevant_qa(query):
    collection = chroma_client.get_collection(name=collection_name_faq, embedding_function=ef)                     # get_collection() => Fetches the FAQ vector DB collection.
    result = collection.query(query_texts=[query], n_results=2)                                                    # Returns top-2 most similar questions (based on embeddings) for a given user query.
    return result 

# ✍️ 6. Generate Answer Using Groq LLM
def generate_answer(query, context):     
                                                                              # Sends the query + retrieved context to GROQ LLM to get a factual answer.
    prompt = f'''Given the following context and question, generate answer based on this context only.
    If the answer is not found in the contex, kinly state "I don't try to make up an answer.
    CONTEXT : {context}
    QUESTION : {query}
    '''
    completion = groq_client.chat.completions.create(                                                               # This allows it access to real-time information and interaction with external environments, providing more accurate, up-to-date, and capable responses than an LLM alone.
        model = os.environ["GROQ_MODEL"],                                                                           # Reads the model name from environment variable (e.g., llama-3-8b)
        messages=[
            {
                'role' :'user',
                'content': prompt
            }
        ]
    )
    return completion.choices[0].message.content

# 🔄 7. Full Retrieval-Augmented Pipeline
def faq_chain(query):
    result = get_relevant_qa(query)                                                                                 # Retrieves the top-matching documents related to the query from the vector database using embeddings.
    context = "".join([r.get('answer') for r in result['metadatas'][0]])                                            # Extrcts answers from FAQ // Extracts the answer field from the metadata of each retrieved document and joins them into a single context string.
    print("Context:", context)                                                                                      # Logs the constructed context for debugging purpose.
    answer = generate_answer(query, context)                                                                        # Sends query + context to LLM and returns the model generated answer.                                                                                                                  
    return answer                                                                                                   # Returns the final answer.

# 🧪 8. Main Function for Testing
if __name__ == "__main__":                                                                                          # Allows script to be run standalone.
    ingest_faq_data(faqs_path)                                                                                      # Ingest CSV content.
    query = "what's your policy on defective on defective products?"                        
    query = "Do you take cash as a payment option?"
    # result = get_relevant_qa(query)
    answer = faq_chain(query)                                                                                       # Executes full retrieval and generation pipleline.
    print('Answer:', answer)                                                                                         # Displays result on console.