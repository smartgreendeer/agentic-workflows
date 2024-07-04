# ai_workflow.py
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from langgraph.graph import END, StateGraph
from  prompt import template,write,answer
import pandas as pd
import sqlite3

load_dotenv()

LLAMA_API = os.getenv("LLAMA_API")
LANGSMITH_API = os.getenv("LANGSMITH_API")

if not LLAMA_API:
    raise Exception("Please set LLAMA_API in .env file")
if not LANGSMITH_API:
    raise Exception("Please set LANGSMITH_APIin .env file")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API
os.environ["LANGCHAIN_PROJECT"] = "RetailX_AI_Assistant"

# Initialize ChatOpenAI model
model = ChatOpenAI(
    openai_api_key=os.getenv("LLAMA_API"),
    openai_api_base="https://api.llama-api.com",
    model="llama3-70b"
)

# Define WorkflowState
class WorkflowState(TypedDict):
    question: str
    plan: str
    can_answer: bool
    sql_query: str
    sql_result: str
    answer: str
    

# Define database description
DB_DESCRIPTION = """You have access to the following tables and columns in a SQLite3 database:

Retail Table
Customer_ID: A unique ID that identifies each customer.
Name: The customer's name.
Gender: The customer's gender: Male, Female.
Age: The customer's age.
Country: The country where the customer resides.
State: The state where the customer resides.
City: The city where the customer resides.
Zip_Code: The zip code where the customer resides.
Product: The product purchased by the customer.
Category: The category of the product.
Price: The price of the product.
Purchase_Date: The date when the purchase was made.
Quantity: The quantity of the product purchased.
Total_Spent: The total amount spent by the customer.
"""

def query_db(query):
    conn = sqlite3.connect('retail.db')
    try:
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()
        
# Action planning step
can_answer_router_prompt = PromptTemplate(
    template=answer,
    input_variables=["data_description", "question"],
)

can_answer_router = can_answer_router_prompt | model | JsonOutputParser()

def check_if_can_answer_question(state):
    result = can_answer_router.invoke({"question": state["question"], "data_description": DB_DESCRIPTION})
    return {"plan": result["reasoning"], "can_answer": result["can_answer"]}

# Skipping workflow steps if the action is not supported
def skip_question(state):
    if state["can_answer"]:
        return "no"
    else:
        return "yes"

# Generating SQL queries with AI
write_query_prompt = PromptTemplate(
    template=write,
    input_variables=["data_description", "question", "plan"],
)

write_query_chain = write_query_prompt | model | JsonOutputParser()

def write_query(state):
    result = write_query_chain.invoke({
        "data_description": DB_DESCRIPTION,
        "question": state["question"],
        "plan": state["plan"]
    })
    sql_query_result = query_db(result["sql_query"])
    
    json_output = sql_query_result.to_json(orient="records")
    
    return {"sql_query": json_output}

# Executing the SQL queries
def execute_query(state):
    query = state["sql_query"]
    try:
        sql_result = query_db(query).to_markdown()
        return {"sql_result": sql_result}
    except Exception as e:
        return {"sql_result": str(e)}

# Generating a human-readable response
write_answer_prompt = PromptTemplate(
    template=template,
    input_variables=["question", "plan", "sql_query", "sql_result"],
)

write_answer_chain = write_answer_prompt | model | JsonOutputParser()

def write_answer(state):
    result = write_answer_chain.invoke({
        "question": state["question"],
        "plan": state["plan"],
        "sql_result": state["sql_result"],
        "sql_query": state["sql_query"]
    })
    return {"answer": result}

# If unable to answer the question
cannot_answer_prompt = PromptTemplate(
    template=template,
    input_variables=["question", "problem"],
)

cannot_answer_chain = cannot_answer_prompt | model | JsonOutputParser()

def explain_no_answer(state):
    result = cannot_answer_chain.invoke({
        "problem": state["plan"],
        "question": state["question"]
    })
    return {"answer": result}

# Define StateGraph for the workflow
workflow = StateGraph(WorkflowState)

workflow.add_node("check_if_can_answer_question", check_if_can_answer_question)
workflow.add_node("write_query", write_query)
workflow.add_node("execute_query", execute_query)
workflow.add_node("write_answer", write_answer)
workflow.add_node("explain_no_answer", explain_no_answer)

workflow.set_entry_point("check_if_can_answer_question")

workflow.add_conditional_edges(
    "check_if_can_answer_question",
    skip_question,
    {
        "yes": "explain_no_answer",
        "no": "write_query",
    },
)

workflow.add_edge("write_query", "execute_query")
workflow.add_edge("execute_query", "write_answer")

workflow.add_edge("explain_no_answer", END)
workflow.add_edge("write_answer", END)

# Compile the workflow
app = workflow.compile()

