from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
# from functions import print_in_color
import os
from dotenv import load_dotenv

load_dotenv()

def chat_model_example():
    chat = ChatOpenAI(temperature=0)

    template = "You are a helpful assistant that translates {input_language} to {output_language}."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    print_in_color(chain.run(input_language="English", output_language="French", text="I love programming."), 'green')


if __name__ == '__main__':
    # code here that should only be executed when chatmodels.py is run directly
    chat_model_example()
