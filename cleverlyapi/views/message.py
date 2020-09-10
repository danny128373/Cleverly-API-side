from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Profile
from ..models import Conversation
from ..models import Message

class MessageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model= Message
        url=serializers.HyperlinkedIdentityField(
            view_name='message',
            lookup_field='id'
        )
        fields=('id', 'url', 'content', 'profile', 'conversation')
        depth=2

class Messages(ViewSet):

    def create(self, request):

        profile = Profile.objects.get(user_id=request.user.id)
        conversation = Conversation.objects.get(request.data['conversation_id'])

        message = Message.objects.create(
            content = request.data['content'],
            profile = profile,
            conversation = conversation
        )

        serializer = MessageSerializer(
            message,
            many=False,
            context={'request':request}
        )

        return Response(serializer.data, content_type='application/json')

    def retrieve(self, request, pk=None):

        try:
            message = Message.objects.get(pk=pk)
            serializer = MessageSerializer(
                message,
                many=False,
                context={'request':request}
            )

            return Response(serializer.data)
        
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        messages = Message.objects.all()
        serializer = MessageSerializer(
            messages,
            many=True,
            context={'request':request}
        )
        return Response(serializer.data)