import base64
from serpy import Serializer, MethodField

class TextDocumentSerializer(Serializer):
    # user_id = MethodField()
    # organization_id = MethodField()
    # description = MethodField()
    content = MethodField()
    # title = MethodField()
    # slug = MethodField()
    created_at = MethodField()

    def get_user_id(self, obj):
        return obj.user.id if obj.user else None

    def get_organization_id(self, obj):
        return obj.organization.id

    def get_description(self, obj):
        return obj.description if obj.description else ""

    def get_content(self, obj):
        return base64.b64decode(obj.content.encode()).decode()

    def get_title(self, obj):
        return obj.title

    def get_slug(self, obj):
        return obj.slug

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")