# Import things that are needed generically
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool

from api.aitools.classes import DocumentReader, ContextAgent, Role
llm = ChatOpenAI(temperature=0)
search = SerpAPIWrapper()
llm_math_chain = LLMMathChain(llm=llm, verbose=True)


def document_reader_tool(question: str):
    # document_reader = DocumentReader()
    return "The Leo DiCaprio's girlfriend is Jenniffer Guzman"

messages = [
    {"content": "You are a helpful assistant that translates English to French.", "role": Role.SYSTEM},
    {"content": "I love programming.", "role": Role.USER},
    {"content": "J'adore la programmation.", "role": Role.ASSISTANT}
]

contextAgent = ContextAgent(context=messages)


tools = [
    Tool.from_function(
        func=document_reader_tool,
        name = "Search",
        description="useful for when you need to answer questions about current events"
        # coroutine= ... <- you can specify an async method if desired as well
    ),
    Tool.from_function(
        func=contextAgent.run,
        name = "ContextAgent",
        description="useful for answer questions about the context of the conversation, you can supposed that you can find the answer here always if its not a search question"
    ),
]




agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)







print(agent.run("Who is Leo DiCaprio's girlfriend?"))


print(agent.run("I love basketball"))