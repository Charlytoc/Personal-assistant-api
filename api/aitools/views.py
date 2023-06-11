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
from .serializers import TextDocumentSerializer
from api.aitools.classes import DocumentReader, ContextAgent, Role

# search = SerpAPIWrapper()
# Create your views here.
def run_home_agent(request):
    
    return render(request, 'home.html')


def playground(request):
    return render(request, 'playground.html')


@csrf_exempt
def conversation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question')
        document_id = data.get('document_id')
        text_document = TextDocument.objects.get(pk=document_id)
        text_document_data = TextDocumentSerializer(text_document).data
        document_reader_tool = DocumentReader(text_document_data["content"])
        answer = document_reader_tool.run(question)
        response_data = {
            "answer": answer
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Invalid request method"})
