from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Conversation
from ..models import Profile


class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for conversations"""

    class Meta:
        model = Conversation
        url = serializers.HyperlinkedIdentityField(
            view_name='conversation',
            lookup_field='id'
        )
        fields = ('id', 'url', 'profile1_id', 'profile2_id')
        depth = 2


class Conversations(ViewSet):

    def create(self, request):
        """
        Handle POST request for a conversation
        Returns: JSON serialized conversation instance
        """
        profile1 = Profile.objects.get(user_id=request.user.id)
        profile2 = Profile.objects.get(user_id=request.data['profile2_id'])

        conversation = Conversation.objects.create(
            content=request.data['content'],
            profile1=profile1,
            profile2=profile2
        )

        serializer = ConversationSerializer(
            conversation,
            context={'request': request}
        )

        return Response(serializer.data, content_type='application/json')

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single conversation
        Returns: JSON serialized conversation instance
        """
        try:
            conversation = Conversation.objects.get(pk=pk)
            serializer = ConversationSerializer(
                conversation,
                many=False,
                context={'request': request}
            )
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        Handle GET requests for conversations
        Returns: Response JSON serialized list of conversations
        """
        conversations = Conversation.objects.all()

        serializer = ConversationSerializer(
            conversations,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)
