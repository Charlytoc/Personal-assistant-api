import base64
from serpy import Serializer, MethodField, Field


class SmallStudyPlanSerializer(Serializer):
    id = Field()
    title = Field()
    description = Field()


class SmallSectionSerializer(Serializer):
    id = Field()
    title = Field()
    objectives = Field()

