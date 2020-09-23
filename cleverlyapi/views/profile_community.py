from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Profile
from ..models import Community
from ..models import ProfileCommunity


class ProfileCommunitySerializer(serializers.ModelSerializer):
    """JSON serializer for profilecommunities"""

    class Meta:
        model = ProfileCommunity
        fields = ('id', 'community', 'profile')
        depth = 1


class ProfileCommunities(ViewSet):

    def create(self, request):
        """
        Handle POST request for a profilecommunities
        Returns: JSON serialized profilecommunities instance
        """
        profile_community = ProfileCommunity()

        profile = Profile.objects.get(pk=request.data['profile_id'])
        profile_community.profile = profile

        community = Community.objects.get(pk=request.data['community_id'])
        profile_community.community = community

        profile_community.save()

        serializer = ProfileCommunitySerializer(
            profile_community,
            context={'request': request}
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single profilecommunities
        Returns: JSON serialized profilecommunities instance
        """
        try:
            profile_community = ProfileCommunity.objects.get(pk=pk)
            serializer = ProfileCommunitySerializer(
                profile_community,
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handles DELETE requests for single profilecommunities"""

        try:
            profile_community = ProfileCommunity.objects.get(pk=pk)
            profile_community.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProfileCommunity.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """
        Handle GET requests for profilecommunities
        Returns: Response JSON serialized list of profilecommunities
        """
        profile_community = ProfileCommunity.objects.all()
        serializer = ProfileCommunitySerializer(
            profile_community,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
