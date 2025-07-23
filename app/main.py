__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# ✅ 1. Imports and Setup
import os                                                          # Allows access to OS-level environment variables like API keys.    
import streamlit as st                                             # Imports Streamlit for building interactive web app.
from pathlib import Path                                           # For working with file paths in an OS-independent way.
from faq import ingest_faq_data, faq_chain                         # Imports logic to process FAQ and answer them. 
from sql import sql_chain                                          # Imoprts a function to process SQL-related queries. 
from smalltalk import talk                                         # imports a function to process small-talk queries
from router import router                                          # Imports a router function to determine query type (FAQ/SQL/etc).

# 🔐 2. API Key Loading
# api_key = os.getenv('GROQ_API_KEY')                                # Enable while using on local machine // Loads the API key from environment variables on your local machine.            
api_key = st.secrets["GROQ_API_KEY"]                             # Enable while deploying in streamlit // When deployed on Streamlit Cloud, use this to securely fetch secrets from .streamlit/secrets.toml.

# 📥 3. Load FAQ Data
faqs_path = Path(__file__).parent/"resources/faq_data.csv"         # Dynamically creates the path to the FAQ CSV file.
ingest_faq_data(faqs_path)                                         # Loads and prepares the FAQ data into memory or a vector store (e.g. ChromaDB) for retrieval.

# 🧠 4. Query Handler Function
def ask(query):
    route = router(query).name                                     # Routes query type: faq, sql, small_talk or others.
    if route == 'faq':
        return faq_chain(query)                                    # Returns/ Runs the query through the FAQ pipeline.
    elif route == 'sql':
        return sql_chain(query)                                    # Returns/ Runs the query through the SQL pipeline.
    elif route == 'small-talk':                                    # name of the route
        return talk(query)                                         # Returns/ Runs the query through the small-talk pipeline.
    else: 
        return f"Route {route} not implemented yet"                # Returns the reponse (for a default message if unsupported).
    
# 💬 5. Streamlit Chat UI Setup 
st.title("E-Commerce Bot")                                         # Diplays the app title.
query = st.chat_input("Write your query")                          # Privides an input box for the user to type a query. 

# 💾 6. Session Storage for Chat Memory
if "messages" not in st.session_state:
    st.session_state["messages"] = []                              # Saves the chat history so messages persist across interactions.

# 📜 7. Display Chat History 
for message in st.session_state.messages:                          # Loops => Iterates over stored messages and displays them in the chat format.
    with st.chat_message(message['role']):                         # can be "user" or "assistant".
        st.markdown(message['content'])                            # The text of the message.

# 🚀 8. Handle New Query 
if query:
    with st.chat_message('user'):                                                 # Show the user's message in chat.
        st.markdown(query)                                                       
    st.session_state.messages.append({'role':'user', 'content':query})  
 
    response = ask(query)                                                         # Call the routing function to get the right response.
    with st.chat_message("assistant"):                                            # Show the bot's response in chat.
        st.markdown(response)
    st.session_state.messages.append({'role':'assistant', 'content':response})    # Update the chat history for persistence
