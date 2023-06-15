import base64
from serpy import Serializer, MethodField, Field

class TextDocumentSerializer(Serializer):
    
    # description = MethodField()
    content = MethodField()
    title = Field()
    # slug = MethodField()
    created_at = Field()

    def get_user_id(self, obj):
        return obj.user.id if obj.user else None

    def get_organization_id(self, obj):
        return obj.organization.id
    
    def get_content(self, obj):
        return base64.b64decode(obj.content.encode()).decode()
    def get_slug(self, obj):
        return obj.slug
class SmallTextDocumentSerializer(Serializer):
    id = Field()
    title = Field()

class SmallAgentSerializer(Serializer):
    id = Field()
    name = Field()
    description = Field()

class SmallConversationSerializer(Serializer):
    id = Field()
    title = Field()

