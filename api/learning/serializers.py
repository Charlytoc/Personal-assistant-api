import base64
from serpy import Serializer, MethodField, Field

class SmallProfileSerializer(Serializer):
    id = Field()
    username = Field()

class SmallStudyPlanSerializer(Serializer):
    id = Field()
    title = Field()
    description = Field()
class BigStudyPlanSerializer(Serializer):
    id = Field()
    title = Field()
    suggested_title = Field()
    description = Field()
    created_by = SmallProfileSerializer()
    ai_description = Field()

class SmallSectionSerializer(Serializer):
    id = Field()
    title = Field()
    objectives = Field()

