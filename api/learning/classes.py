from langchain.chat_models import ChatOpenAI
from langchain import LLMChain

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate
)

import os
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback

class SinglePromptAgent:
    def __init__(self,
                temperature: int = 0, 
                template: str = 
                '''
                You objective is: {objective}
                Your answer must have the following structure
                _start_ 
                {response_structure}
                _end_

                The _start_ and _end_ tags are mandatory. 
                Use this context: {context} to give your answer
                '''):
        
        self.system_template = template
        # The temperature parameter controls the randomness of the model's output, with a lower temperature resulting in more deterministic output.
        self.chat = ChatOpenAI(temperature=temperature)

        self.system_message_prompt = SystemMessagePromptTemplate.from_template(self.system_template)

        self.start_tag = "_start_"
        self.end_tag = "_end_"

        self.chat_prompt = ChatPromptTemplate.from_messages(
            # [self.system_message_prompt, self.user_message_prompt]
            [self.system_message_prompt]
        )
        # Create an instance of LLMChain
        self.chain = LLMChain(llm=self.chat, prompt=self.chat_prompt)

    # This is the main entry point of the class
    def extract_response(self, text):
        try:
            result = text.split(self.start_tag)[1].split(self.end_tag)[0]
        except IndexError:
            result = ""
        return result
    
    def run(self,**args):
        agent_response = self.chain.run(
            **args
        )
        agent_response = self.extract_response(agent_response)
        return agent_response


