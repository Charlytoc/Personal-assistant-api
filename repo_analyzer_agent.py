import os
import subprocess
import shutil
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from functions import print_in_color
import os

from typing import Any, Dict, List, Optional
import logging
from typing import List, Optional
from langchain.indexes import VectorstoreIndexCreator

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders.helpers import detect_file_encodings
from langchain.chat_models import ChatOpenAI


logger = logging.getLogger(__name__)


from langchain.document_loaders import TextLoader
from dotenv import load_dotenv
load_dotenv()



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
            file_contents += f"{indentation}## {item}\n```\n{content}\n```\n\n"
        elif os.path.isdir(item_path):
            file_contents += generate_file_contents(item_path, os.listdir(item_path), indentation)
    return file_contents

# Example usage
repo_url = "https://github.com/breatheco-de/dataflow-project-template.git"
target_dir = "example-repo"
explore_items = ["README.md", "pipelines"]
output_file = "project_structure.md"

clone_and_explore_repository(repo_url, target_dir, explore_items, output_file=output_file)

loader = TextLoader("./project_structure.md")
# loader.load()
chat = ChatOpenAI(temperature=0)
index = VectorstoreIndexCreator().from_loaders([loader])

question_to_answer = "Explain me how to use the repo"
print_in_color(index.query(question_to_answer, llm=chat))

question_to_answer_2 = "Make a better readme.md for the repository"
print_in_color(index.query(question_to_answer_2, llm=chat))

