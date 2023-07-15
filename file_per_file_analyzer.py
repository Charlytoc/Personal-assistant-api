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

load_dotenv()
logger = logging.getLogger(__name__)


class SinglePromptAgent:
    def __init__(
        self,
        system_prompt: str = '''
        You are a special code reviewer, your task is provide useful reviews about a code inside a repository\n
        Provide reviews about improvements in the code without editing the code yourself, just tell about \n
        the changes that can be made to have a cleaner, optimized and understandable code

        Provide the reviews in the text format:

        _start_

        -rs- review about something -re-
        -rs- another review about something else in the code -re-
        
        _end_

        '''
    ) -> None:
        self._system_prompt = system_prompt
        self.chat = ChatOpenAI(temperature=0)

    def run(self, question: str):
        messages: list[BaseMessage] = [
            SystemMessage(content=self._system_prompt),
            HumanMessage(content=question)
        ]

        response = self.chat(messages).content
        return response






def clone_and_explore_repository(repo_url, target_dir, explore_items, output_file):

    # Create a new directory
    os.makedirs(target_dir, exist_ok=True)

    # Clone the repository into the target directory
    subprocess.run(["git", "clone", repo_url, target_dir])

    # Explore and copy the content of specified files or directories
    markdown_content = "# Project structure\n\n"
    markdown_content += generate_directory_structure(target_dir, explore_items)
    markdown_content += "\n# Project files:\n\n"
    markdown_content += generate_file_contents(target_dir, explore_items)

    # Write markdown content to the output file
    with open(output_file, 'w') as file:
        file.write(markdown_content)

    # Remove the cloned directory
    shutil.rmtree(target_dir)

def generate_directory_structure(directory, explore_items, indentation=""):
    directory_structure = ""  
    for item in explore_items:
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            directory_structure += f"{indentation}- {item}\n"
            directory_structure += generate_directory_structure(item_path, os.listdir(item_path), indentation + "    ")
            directory_structure += generate_file_contents(item_path, os.listdir(item_path), indentation + "        ")
    return directory_structure

def generate_file_contents(directory, explore_items, indentation=""):
    file_contents = ""
    for item in explore_items:
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            with open(item_path, 'r') as file:
                content = file.read()
                if content.strip():  
                    review_agent = SinglePromptAgent()
                    print_in_color(review_agent.run(question=content))

                    file_contents += f"{indentation}## {item}\n```\n{content}\n```\n\n"
        elif os.path.isdir(item_path):
            file_contents += generate_file_contents(item_path, os.listdir(item_path), indentation)
    return file_contents

# Example usage
repo_url = "https://github.com/Charlytoc/dataflow-project-events.git"
target_dir = "example-repo"
explore_items = ["README.md", "pipelines"]
output_file = "project_structure.md"

clone_and_explore_repository(repo_url, target_dir, explore_items, output_file=output_file)



# loader = TextLoader("./project_structure.md")
# loader.load()


# question_to_answer = "Make a summary of the repo, also make mention of the improvements we can make"

# chat = ChatOpenAI(temperature=0)
# index = VectorstoreIndexCreator().from_loaders([loader])

# print(index.query(question_to_answer, llm=chat))