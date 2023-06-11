from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage, 
    BaseMessage
)
from api.aitools.classes import Role
from dotenv import load_dotenv
load_dotenv()




messages = [
    {"content": "You are a helpful assistant that translates English to French.", "role": Role.SYSTEM},
    {"content": "I love programming.", "role": Role.USER},
    {"content": "J'adore la programmation.", "role": Role.ASSISTANT}
]



class ContextAgent():
    def __init__(self, system_message: str = "You are a helpful assistant that follows the conversation flow", context: list[dict] = [], openai_api_key:str = '') -> None:
        self.messages: list[BaseMessage] = []
        self.append_message(content=system_message, role=Role.SYSTEM)
        for message in context:
            self.append_message(content=message["content"], role=message["role"])
        self.chat = ChatOpenAI(temperature=0)

    def append_message(self, content:str, role:str):
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

contextAgent = ContextAgent(context=messages)
print(contextAgent.run(question="I want to play basket ball"))