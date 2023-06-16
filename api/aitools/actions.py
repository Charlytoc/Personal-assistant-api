from .serializers import SmallAgentSerializer, SmallTextDocumentSerializer, SmallConversationSerializer
from .models import Agent, TextDocument
from datetime import datetime
from .models import Conversation
from ..authenticate.models import Token
from .classes import DocumentReader


def get_serialized_agents():
    agents = Agent.objects.all()
    serializer = SmallAgentSerializer(agents, many=True)
    serialized_data = serializer.data
    return serialized_data


def get_serialized_documents():
    documents = TextDocument.objects.all()
    serializer = SmallTextDocumentSerializer(documents, many=True)
    serialized_data = serializer.data
    
    return serialized_data




from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def get_user_from_token(token):
    try:
        token_obj = Token.objects.get(key=token)
        return token_obj.user
    except ObjectDoesNotExist:
        return None
    

def get_user_conversations(user):
    conversations = Conversation.objects.filter(user=user)
    return conversations


def serialize_conversations(conversations):
    return SmallConversationSerializer(conversations, many=True).data
    

def get_agent_by_id(agent_id: int):
    slug = get_agent_function_slug(agent_id)
    agent = get_agent_by_slug(slug)
    return agent


def get_agent_function_slug(agent_id):
    try:
        agent = Agent.objects.get(id=agent_id)
        return agent.function_slug
    except ObjectDoesNotExist:
        # Agent with the given ID does not exist
        return None

def get_agent_by_slug(agent_slug: str):
    agents = {
        "document_reader": lambda: DocumentReader
    }
    return agents[agent_slug]


def create_conversation(user):
    conversation = Conversation.objects.create(
        title="New Conversation",
        user=user,
        started_at=datetime.now(),
    )
    return conversation


def get_message_count(conversation):
    return conversation.message_set.count()

def user_has_empty_conversation(user: User) -> bool:
    # Get all the user conversations
    conversations = Conversation.objects.filter(user=user)
    # Loop for each conversation
    for conversation in conversations:
        # If a conversation has 0 messages, return True
        if conversation.message_set.count() == 0:
            return True
    # Return False if no empty conversations found
    return False


def get_empty_conversation_by_user(user: User) -> Conversation:
    # Check if the user has an empty conversation
    has_empty_conversation = user_has_empty_conversation(user)

    if has_empty_conversation:
        # If the user has an empty conversation, return that conversation
        empty_conversation = Conversation.objects.filter(user=user, message__isnull=True).first()
        return empty_conversation
    else:
        # Else create a new conversation for the user
        conversation = create_conversation(user)
        return conversation