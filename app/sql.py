# ✅ 1. Import Modules and Load Environment Variables
from groq import Groq                                                          # Imports Groq LLM client.   
import os                                                                      # Allows access to os-level environment variables like API keys./ Access environment variables like API keys.
import re                                                                      # Regular expressions.
import sqlite3                                                                 # Used to connect and query the SQLite database and convert result to DataFrame.
import pandas as pd                                                            # Reading FAQ data from CSV.
from pathlib import Path                                                       # OS-independent file path handling.
from dotenv import load_dotenv                                                 # Load .env file into Python environment.
from pandas import DataFrame                                                   # query the SQLite database and convert result to a DataFrame.

load_dotenv()                                       
GROQ_MODEL = os.environ['GROQ_MODEL']                                          # Safely reads the model name and API key from environment.
api_key = os.getenv("GROQ_API_KEY")

# 📍 2. Set Path and Initialize Groq Client
db_path = Path(__file__).parent/"db.sqlite"
client_sql = Groq(api_key=api_key)

#🧾 3. SQL Prompt Template for LLM                                             #  🧠 LLM Role => Pretends to be an expert at translating natural language to SQL , 🧱 Schema => 	Describes the structure of the SQLite database ,  🔍 Tip => Emphasizes use of %LIKE% for brand search , 🔖 Format => Always returns SQL query inside <SQL> ... </SQL> tags 
sql_prompt = """You are an expert in understanding the database schema and generating SQL queries for a natural language question asked
pertaining to the data you have. The schema is provided in the schema tags. 
<schema> 
table: product                                                                     

fields: 
product_link - string (hyperlink to product)	
title - string (name of the product)	
brand - string (brand of the product)	
price - integer (price of the product in Indian Rupees)	
discount - float (discount on the product. 10 percent discount is represented as 0.1, 20 percent as 0.2, and such.)	
avg_rating - float (average rating of the product. Range 0-5, 5 is the highest.)	
total_ratings - integer (total number of ratings for the product)

</schema>
Make sure whenever you try to search for the brand name, the name can be in any case. 
So, make sure to use %LIKE% to find the brand in condition. Never use "ILIKE". 
Create a single SQL query for the question provided. 
The query should have all the fields in SELECT clause (i.e. SELECT *)

Just the SQL query is needed, nothing more. Always provide the SQL in between the <SQL></SQL> tags."""

# ✍️ 4. Prompt for Natural Language Summarization
comprehension_prompt = """You are an expert in understanding the context of the question and replying based on the data pertaining to the question provided. You will be provided with Question: and Data:. The data will be in the form of an array or a dataframe or dict. Reply based on only the data provided as Data for answering the question asked as Question. Do not write anything like 'Based on the data' or any other technical words. Just a plain simple natural language response.
The Data would always be in context to the question asked. For example is the question is “What is the average rating?” and data is “4.3”, then answer should be “The average rating for the product is 4.3”. So make sure the response is curated with the question and data. Make sure to note the column names to have some context, if needed, for your response.
There can also be cases where you are given an entire dataframe in the Data: field. Always remember that the data field contains the answer of the question asked. All you need to do is to always reply in the following format when asked about a product: 
Product title, price in indian rupees, discount, and rating, and then product link. Take care that all the products are listed in list format, one line after the other. Not as a paragraph.
For example:
1. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>
2. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>
3. Campus Women Running Shoes: Rs. 1104 (35 percent off), Rating: 4.4 <link>

"""
# 🔄 5. SQL Generation Function
def generate_sql_query(question):                                            # This allows it access to real-time information and interaction with external environments, providing more accurate, up-to-date, and capable responses than an LLM alone.
    chat_completion = client_sql.chat.completions.create(                    # Sends schema prompt + user question to LLM. 
        messages=[
            {
                "role":'system',
                "content": sql_prompt,
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        model = os.environ["GROQ_MODEL"],
        temperature=0.2,                                                       # Temperature makes the output more deterministic.
        max_tokens=1024
    )
    return chat_completion.choices[0].message.content

# 🔎 6. SQL Execution Function
def run_query(query):  
    if query.strip().upper().startswith('SELECT'):                             # Checks if query starts with SELECT.  
        with sqlite3.connect(db_path) as conn:                         
            df = pd.read_sql_query(query, conn)                                # Uses pandas.read_sql_query() to get query results as a DataFrame.
            return df                                                          # Returns data for further summerization. 

# 🧠 7. Human-Like Answer Generation                                           # LLM receives : QUESTION: ...DATA: ...
def data_comprehension(question, context):                                      # This allows it access to real-time information and interaction with external environments, providing more accurate, up-to-date, and capable responses than an LLM alone.
    chat_completion = client_sql.chat.completions.create(
        messages=[
            {
                "role":"system",
                "content":comprehension_prompt,                                 # Uses comprehension prompt for summerization.                      
            },
            {
                "role": "user",
                "content": f"QUESTION: {question}. DATA: {context}",
            }
        ],
        model = os.environ["GROQ_MODEL"],
        temperature=0.2,
        max_tokens=1024
    )
    return chat_completion.choices[0].message.content                           # Returns answer in plain language (e.g. product listings).

# 🔁 8. sql_chain() - Complete Pipeline
def sql_chain(question):                
    sql_query = generate_sql_query(question)                                     # Gets SQL from LLM 
    pattern = "<SQL>(.*?)</SQL>"                                                 # using regex
    matches = re.findall(pattern, sql_query, re.DOTALL)


    if len(matches) == 0:
        return "Sorry, LLM is not able to generate a query for your question."
    print(matches[0].strip())

    response = run_query(matches[0].strip())                                     # Executes SQL on db.sqlite
    if response is None:
        return "Sorry, there was a problem executing SQL query"
    
    context = response.to_dict(orient='records')

    answer = data_comprehension(question, context)                               # Generates a natural response 
    return answer                                                                # Returns final answer

# 🧪 9. Main Function – Test Code
if __name__ == "__main__":
    # question = "All shoes with rating higher than 4.5 and total number of reviews greater than 500"        
    # sql_query = generate_sql_query(question)                                                               
    # print(sql_query)
    # question = "Show top 3 shoes in descending order of rating"               # Defines test input                                    
    question = "Show me 3 running shoes for woman"
    # question = "sfsdfsddsfsf"
    answer = sql_chain(question)                                              # Runs the complete pipeline
    print(answer)                                                             # Displays final summarized result



'''
--------------------------
EXPLANATION of CODE BLOCK
-------------------------


# 🧾 3. SQL Prompt Template for LLM
| Role        | Explanation                                                     |
| ----------- | --------------------------------------------------------------- |
| 🧠 LLM Role | Pretends to be an expert at translating natural language to SQL |
| 🧱 Schema   | Describes the structure of the SQLite database                  |
| 🔍 Tip      | Emphasizes use of `%LIKE%` for brand search                     |
| 🔖 Format   | Always returns SQL query inside `<SQL> ... </SQL>` tags         |


# ✍️ 4. Prompt for Natural Language Summarization
| Role        | Explanation                                                |
| ----------- | ---------------------------------------------------------- |
| 🤖 LLM Role | Generates human-readable output based on returned SQL data |
| 📄 Input    | Provides Question + Data as JSON/array                     |
| 🎯 Output   | Simple human response formatted as product list if needed  |



'''