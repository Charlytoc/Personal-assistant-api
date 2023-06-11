from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from functions import print_in_color
import os
from dotenv import load_dotenv

from typing import Any, Dict, List, Optional
import logging
from typing import List, Optional
from langchain.indexes import VectorstoreIndexCreator

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.document_loaders.helpers import detect_file_encodings


from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage, 
    BaseMessage
)
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


from langchain.document_loaders import TextLoader
load_dotenv()

class CustomTextLoader(BaseLoader):
    """Load plain text and metadata dictionary."""

    def __init__(
        self,
        plain_text: str,
        metadata: Optional[Dict[str, Any]] = None,
        encoding: Optional[str] = None,
        autodetect_encoding: bool = False,
    ):
        """Initialize with plain text and metadata."""
        self.plain_text = plain_text
        self.metadata = metadata or {}
        self.encoding = encoding
        self.autodetect_encoding = autodetect_encoding

    def load(self) -> List[Document]:
        """Load from plain text."""
        text = self.plain_text
        if self.encoding:
            try:
                text = text.encode(self.encoding).decode(self.encoding)
            except UnicodeDecodeError as e:
                if self.autodetect_encoding:
                    detected_encodings = detect_file_encodings(text)
                    for encoding in detected_encodings:
                        logger.debug("Trying encoding: ", encoding)
                        try:
                            text = text.encode(encoding).decode(encoding)
                            break
                        except UnicodeDecodeError:
                            continue
                else:
                    raise RuntimeError(f"Error loading plain text") from e

        metadata = self.metadata
        return [Document(page_content=text, metadata=metadata)]

import logging

class DocumentReader():
    def __init__(self, document_text: str, openai_api_key: str) -> None:
        os.environ['OPENAI_API_KEY'] = openai_api_key
        self.loader = CustomTextLoader(document_text)
        self.index = VectorstoreIndexCreator().from_loaders([self.loader])
        logging.info("Index created successfully")
        
    def run(self, question_to_answer: str):
        try:
            answer = self.index.query(question_to_answer)
            logging.info(f"Answer found for question: {question_to_answer}")
            del os.environ['OPENAI_API_KEY']
            return answer
        except Exception as e:
            logging.error(f"Error occurred while querying index: {e}")
            return None
        
class Role():
    USER = 'USER'
    SYSTEM = 'SYSTEM'
    ASSISTANT = 'ASSISTANT'




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

