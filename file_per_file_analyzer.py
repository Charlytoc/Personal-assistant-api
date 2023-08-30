import os
import subprocess
import shutil
from typing import Any, Dict, List, Optional
import logging
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from functions import print_in_color
from langchain.indexes import VectorstoreIndexCreator
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders.helpers import detect_file_encodings
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, BaseMessage
import os
import random
from git import Repo
from termcolor import colored
load_dotenv()
logger = logging.getLogger(__name__)
class SinglePromptAgent:
        def __init__(self, system_prompt: str = ''' You are a special code reviewer, your task is provide useful reviews about a code inside a repository\n Provide reviews about improvements in the code without editing the code yourself, just tell about \n the changes that can be made to have a cleaner, optimized and understandable code, Provide the reviews in the text format:, _start_, -rs- review about something -re- -rs- another review about something else in the code -re- _end_, ''' ) -> None:
                self._system_prompt = system_prompt
                self.chat = ChatOpenAI(temperature=0)
        def run(self, question: str):
                messages: list[BaseMessage] = [ SystemMessage(content=self._system_prompt), HumanMessage(content=question) ]
                response = self.chat(messages).content
                return response
def clone_and_print_files_in_random_colors(github_url: str, target_dir: str) -> None:
        Repo.clone_from(github_url, target_dir)
        colors = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
        for foldername, subfolders, filenames in os.walk(target_dir):
                for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        with open(file_path, 'r') as file:
                                file_content = file.read()
                        color = random.choice(colors)
                        print(colored(f'File Name: {filename}', color))
                        print(colored(f'File Content: {file_content}', color))
# Other functions and code omitted for brevity
# Example usage
repo_url = "https://github.com/Charlytoc/dataflow-project-events.git"
target_dir = "example-repo"
explore_items = ["README.md", "pipelines"]
clone_and_print_files_in_random_colors(repo_url, target_dir)
# Rest of the code omitted for brevity

loader = TextLoader("./project_structure.md")
loader.load()


question_to_answer = "Make a summary of the repo, also make mention of the improvements we can make"

# chat = ChatOpenAI(temperature=0)
# index = VectorstoreIndexCreator().from_loaders([loader])

# print(index.query(question_to_answer, llm=chat))