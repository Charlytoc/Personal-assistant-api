import uuid
from typing import Dict, Union

import structlog
from langchain.callbacks import get_openai_callback
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool

import settings
from src.agents.text_to_sql import text_to_sql_executor_custom, Text2SQLResult
from src.chains.router import RouterChain
from src.database import pinecone_db
from src.database.pinecone_db import VectorSearchResult
from src.agents.clickhouse_retriever import clickhouse_retriever_tool

logger = structlog.get_logger(__name__)

 




import settings
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from .text_to_sql import Text2SQLResult
import structlog
logger = structlog.get_logger(__name__)

from langchain.chat_models import ChatOpenAI
# from langchain import LLMChain
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage, 
    BaseMessage
)
import os
from dotenv import load_dotenv
from .text2sql.chain import get_client

load_dotenv()

        
class Role():
    USER = 'USER'
    SYSTEM = 'SYSTEM'
    ASSISTANT = 'ASSISTANT'


class SinglePromptAgent:
    def __init__(self, system_prompt: str = "You are an useful assistant", openai_api_key: str = settings.OPENAI_API_KEY) -> None:
        self.messages: list[BaseMessage] = []
        self.chat = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)
        self.append_message(content=system_prompt)

    def append_message(self, content:str, role:str = Role.SYSTEM):
        options = {
            Role.ASSISTANT: lambda: self.messages.append(AIMessage(content=content)),
            Role.USER: lambda: self.messages.append(HumanMessage(content=content)),
            Role.SYSTEM: lambda: self.messages.append(SystemMessage(content=content)),
        }
        options[role]()

    def run(self, question: str):
        self.append_message(content=question, role=Role.USER)
        response = self.chat(self.messages).content
        return response



def get_query_result(query:str, clickhouse_uri=settings.CLICKHOUSE_URI):

    profile_client = get_client(clickhouse_uri)
    

    result_rows = profile_client.query(query)
  
    profile_client.close()

    return Text2SQLResult(
                query, result_rows.result_rows, result_rows.column_names
            )

def extract_text(text):
    start_tag = "-start_query-"
    end_tag = "-end_query-"

    start_index = text.find(start_tag) + len(start_tag)
    end_index = text.find(end_tag)

    if start_index != -1 and end_index != -1:
        extracted_text = text[start_index:end_index].strip()
        return extracted_text
    else:
        return None

def print_in_red(text):
    red_text = '\033[91m' + text + '\033[0m'
    print(red_text)

def clickhouse_retriever_tool(query: str):
    _system_prompt = '''
    You are an especial Clickhouse employee with just one task:\n

    Ensure a SQL query its well written to Clickhouse sintax, you will receive: \n

    One or two queries and maybe a question, you need to return just the final SQL query without error or comments\n
    Ensure of returning just ONE SQL query, always needs to be the last or most appropiate each case\n
    with the following tags, ensuring it has both start and end tags:
    
    -start_query-

    Here needs to be the correct sql query

    -end_query-
    '''
    clickhouse_agent = SinglePromptAgent(system_prompt=_system_prompt)
    sql_query = clickhouse_agent.run(question=query)

    cleaned_sql_query = extract_text(sql_query)
    return get_query_result(query=cleaned_sql_query)



Tool(
            name='clickhouse_retriever',
            description=(
            "Use this tool only when user input is SQL query without additional text. "
            "SQL usually start with SELECT or WITH. "
            "Validate SQL query and this query is not have appropriate format for SQL — don't use this tool."
            "IMPORTANT: This tool only for execution SQL queries. Don't use it for other purposes. "
            "You must use this tool if in the user input is SQL formatted query."
            ),
            func=clickhouse_retriever_tool
        ),

