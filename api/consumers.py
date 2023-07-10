import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json
from api.aitools.views import async_get_document_reader_answer
from django.core.exceptions import ObjectDoesNotExist

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        question = text_data_json.get('question')
        conversation_id = text_data_json.get('conversation_id')
        document_id = text_data_json.get('document_id')
        agent_id = text_data_json.get('agent_id')

        # answer = get_document_reader_answer(question=question, document_id=document_id)
        answer = await async_get_document_reader_answer(question=question, document_id=document_id)
        # Here, process the message and generate your response
        # For simplicity, I am echoing back the question

        await self.send(text_data=json.dumps({
            'message': answer
        }))
        # await self.send(text_data=json.dumps({
        #     'message': 'THIS IS A SECOND LANGUAGE'
        # }))

