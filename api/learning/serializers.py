import base64
from serpy import Serializer, MethodField, Field

class SmallProfileSerializer(Serializer):
    id = Field()
    username = Field()

class SmallStudyPlanSerializer(Serializer):
    id = Field()
    title = Field()
    description = Field()

class SmallSectionSerializer(Serializer):
    id = Field()
    title = Field()
    objective = Field()



class BigStudyPlanSerializer(Serializer):
    id = Field()
    title = Field()
    slug= Field()
    sections = MethodField()
    suggested_title = Field()
    description = Field()
    created_by = SmallProfileSerializer()
    ai_description = Field()

    def get_sections(self, obj):
        sections = obj.section_set.all()
        sections_data = SmallSectionSerializer(sections, many=True).data
        return sections_data
    
