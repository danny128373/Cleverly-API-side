from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Profile
from ..models import Relationship


class RelationshipSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for comments"""

    class Meta:
        model = Relationship
        url = serializers.HyperlinkedIdentityField(
            view_name='relationship',
            lookup_field='id'
        )
        fields = ('id', 'url', 'friender', 'friendee', 'status')
        depth = 2


class Relationships(ViewSet):

    def create(self, request):
        """
        Handle POST request for a comment
        Returns: JSON serialized comment instance
        """
        friender = Profile.objects.get(user_id=request.user.id)
        friendee = Profile.objects.get(user_id=request.data['friendee'])

        relationship = Relationship.objects.create(
            friender=friender,
            friendee=friendee,
            status=request.data['status']
        )

        serializer = RelationshipSerializer(
            relationship, context={'request': request})

        return Response(serializer.data, content_type='application/json')

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single comment
        Returns: JSON serialized comment instance
        """
        try:
            relationship = Relationship.objects.get(pk=pk)
            serializer = RelationshipSerializer(
                relationship,
                many=False,
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        Handling a PUT request for a comment
        Returns: Empty body with 204 status code
        """
        relationship = Relationship.objects.get(pk=pk)
        relationship.status = request.data['status']
        relationship.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handles DELETE requests for single comment"""

        try:
            relationship = Relationship.objects.get(pk=pk)
            relationship.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Relationship.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """
        Handle GET requests for comments
        Returns: Response JSON serialized list of comments
        """
        relationships_friender = Relationship.objects.filter(
            friender=request.user.id)
        relationships_friendee = Relationship.objects.filter(
            friendee=request.user.id)
        relationships = relationships_friendee + relationships_friender

        serializer = RelationshipSerializer(
            relationships,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)
