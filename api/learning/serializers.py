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

class ProfileSerializer(Serializer):
        # user = Field()
        username = Field()
        # communities = MethodField()
        # is_public = Field()
        # biography = Field()
        # profile_type = Field()
        # character = Field()
        # created_at = Field()
        # updated_at = Field()
        def get_communities(self, obj):
                return [community.name for community in obj.communities.all()]
        
class SmallProfileSerializer(Serializer):
        # user = Field()
        username = Field()
        # communities = MethodField()
        # is_public = Field()
        # biography = Field()
        # profile_type = Field()
        # character = Field()
        # created_at = Field()
        # updated_at = Field()
        def get_communities(self, obj):
                return [community.name for community in obj.communities.all()]
        

class CommentSerializer(Serializer):
        id = Field()
        profile = MethodField()
        text = Field()
        created_at = Field()
        updated_at = Field()
        def get_profile(self, obj):
                return SmallProfileSerializer(obj.profile).data
        

class DiscussionSerializer(Serializer):
        id = Field()
        # created_by = MethodField()
        # topic = MethodField()
        text =Field()
        created_at = Field()
        updated_at = Field()
        comments = MethodField()
        def get_comments(self, obj):
                return [CommentSerializer(comment).data for comment in obj.comment_set.all()]

class TopicSerializer(Serializer):
        id = Field()
        title = Field()
        explanation = Field()
        # section = MethodField()
        objective = Field()
        # created_by = MethodField()
        # created_at = Field()
        # updated_at = Field()
        discussions = MethodField()

        def get_discussions(self, obj):
            _discussions = obj.discussion_set.all()
            discussions_data = DiscussionSerializer(_discussions, many=True).data
            return discussions_data

class BigSectionSerializer(Serializer):
    id = Field()
    title = Field()
    objective = Field()
    topics = MethodField()
    def get_topics(self, obj):
        topics = obj.topic_set.all()
        topics_data = TopicSerializer(topics, many=True).data
        return topics_data
