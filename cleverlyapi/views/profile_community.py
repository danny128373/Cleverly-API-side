from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Profile
from ..models import Community
from ..models import ProfileCommunity

class ProfileCommunitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProfileCommunity
        url = serializers.HyperlinkedIdentityField(
            view_name='profilecommunity',
            lookup_field='id'
        )
        fields=('id','url', 'community', 'profile')
        depth=1
    
class ProfileCommunities(ViewSet):

    def create(self, request):
        profile_community = ProfileCommunity()

        profile = Profile.objects.get(pk=request.data['profile_id'])
        profile_community.profile=profile

        community = Community.objects(pk=request.data['community_id'])
        profile_community.community = community

        profile_community.save()

        serializer = ProfileCommunitySerializer(
            profile_community,
            context={'request':request}
        )

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            profile_community = ProfileCommunity.objects.get(pk=pk)
            serializer = ProfileCommunitySerializer(
                profile_community,
                context={'request':request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):

        try:
            profile_community = ProfileCommunity.objects.get(pk=pk)
            profile_community.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProfileCommunity.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message':ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        profile_community= ProfileCommunity.objects.all()
        serializer = ProfileCommunitySerializer(
            profile_community,
            many=True,
            context={'request':request}
        )
        return Response(serializer.data)