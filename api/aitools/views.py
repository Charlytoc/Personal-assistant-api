import json
from django.shortcuts import render
from .classes import DocumentReader, ContextAgent
# Import things that are needed generically
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import TextDocument
from ..authenticate.models import ProviderCredentials
from .serializers import TextDocumentSerializer
from api.aitools.classes import DocumentReader, ContextAgent, Role
from .actions import (
    get_serialized_agents, get_serialized_documents, get_user_from_token, get_user_conversations, serialize_conversations, create_conversation,
                      get_agent_by_id, get_empty_conversation_by_user)

from .classes import DocumentReader
from asgiref.sync import sync_to_async
# Create your views here.
def run_home_agent(request):
    return render(request, 'home.html')


def start_conversation(request):
    token = request.GET.get('token', '')
    user = get_user_from_token(token)
    if not user:
        response_data = {
            'error': 'Authentication required. You must be authenticated to use this view.'
        }
        return JsonResponse(response_data, status=401)
    
    conversation = get_empty_conversation_by_user(user)
    agents = get_serialized_agents()
    documents = get_serialized_documents()
    conversations = get_user_conversations(user)
    serialized_conversations = serialize_conversations(conversations)

    data = {
        "agents": agents,
        "documents": documents,
        "user": user,
        "conversations": serialized_conversations,
        "conversation_id": conversation.id
    }
    return render(request, 'playground.html', data)


@csrf_exempt
def conversation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question')
        document_id = data.get('document_id')
        text_document = TextDocument.objects.get(pk=document_id)
        openai_key = ProviderCredentials.objects.get(organization=text_document.organization)
        text_document_data = TextDocumentSerializer(text_document).data
        document_reader_tool = DocumentReader(text_document_data["content"], openai_api_key=openai_key.key)
        answer = document_reader_tool.run(question)
        response_data = {
            "answer": answer
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Invalid request method"})


@csrf_exempt
def follow_conversation(request, conversation_id):
    if request.method == "POST":
        # Catch error if the token is None, return a Json error
        auth_header = request.headers['Authorization']
        token = auth_header.split(' ')[1] 
        # print(f'This is the conversation ID: {conversation_id}')
        # Get the data from the request body and return a json if any miss indication which fields are needed
        data = json.loads(request.body)
        question = data.get('question')
        document_id = data.get('document_id')
        # agent_id = data.get('agent_id')

        answer = get_document_reader_answer(question=question, document_id=document_id)
        # get the agent model, return an error if something if the agent not exist
        # agent = get_agent_by_id(agent_id)
        
        response_data = {
            "answer": answer
        }
        return JsonResponse(response_data)

# @sync_to_async
def get_document_reader_answer(question: str, document_id: int):
    text_document = TextDocument.objects.get(pk=document_id)
    # get the credentials
    credentials = ProviderCredentials.objects.get(organization=text_document.organization)
    # get the content from the document
    text_document_data = TextDocumentSerializer(text_document).data
    document_reader_tool = DocumentReader(text_document_data["content"], openai_api_key=credentials.key)
    answer = document_reader_tool.run(question)
    return answer
