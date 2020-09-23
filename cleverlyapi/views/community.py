from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Profile
from ..models import Community
from ..models import ProfileCommunity


class CommunitySerializer(serializers.ModelSerializer):
    """JSON serializer for communities"""

    class Meta:
        model = Community
        fields = ('id', 'name', 'description', 'image', 'profile')
        depth = 2


class Communities(ViewSet):

    def create(self, request):
        """
        Handle POST request for a community
        Returns: JSON serialized community instance
        """
        profile = Profile.objects.get(pk=request.data['profile_id'])
        community = Community.objects.create(
            name=request.data['name'],
            description=request.data['description'],
            image=request.data['image'],
            profile=profile
        )

        profile_community = ProfileCommunity.objects.create(
            profile=profile,
            community=community
        )

        serializer = CommunitySerializer(
            community, context={'request': request})
        return Response(serializer.data, content_type='application/json')

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single community
        Returns: JSON serialized community instance
        """
        try:
            community = Community.objects.get(pk=pk)
            serializer = CommunitySerializer(
                community,
                many=False,
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        Handling a PUT request for a community
        Returns: Empty body with 204 status code
        """
        community = Community.objects.get(pk=pk)
        community.name = request.data['name']
        community.description = request.data['description']
        community.image = request.data['image']
        community.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handles DELETE requests for single community"""
        try:
            community = Community.objects.get(pk=pk)
            community.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Community.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """
        Handle GET requests for communities
        Returns: Response JSON serialized list of communities
        """
        communities = Community.objects.all()
        name = self.request.query_params.get('search', None)
        if name is not None:
            communities = communities.filter(name__contains=name)
        serializer = CommunitySerializer(
            communities, many=True, context={'request': request})
        return Response(serializer.data)
