import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json

from django.core.exceptions import ObjectDoesNotExist

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    # async def disconnect(self, close_code):
    #     pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        print(f'Received message: {message}')  # print the message to console

        # Respond with 'Hello, World' regardless of incoming message
        await self.send(text_data=json.dumps({
            'message': 'Hello, World'
        }))


class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        print(f'This is the conversation ID: {self.conversation_id}')
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Parse the data from the WebSocket
        data = json.loads(text_data)
        question = data.get('question')
        document_id = data.get('document_id')
        agent_id = data.get('agent_id')

        try:
            # get the agent model, return an error if something if the agent not exist
            # agent = get_agent_by_id(agent_id)

            text_document = TextDocument.objects.get(pk=document_id)

            # get the credentials
            credentials = ProviderCredentials.objects.get(organization=text_document.organization)
        
            # get the content from the document
            text_document_data = TextDocumentSerializer(text_document).data
        
            document_reader_tool = DocumentReader(text_document_data["content"], openai_api_key=credentials.key)
            answer = document_reader_tool.run(question)
            response_data = {
                "answer": answer
            }
        except ObjectDoesNotExist as e:
            # Handle error here, for example, by sending an error message back
            response_data = {"error": str(e)}

        # Send the response data back over the WebSocket
        await self.send_json(response_data)