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

    class Meta:
        model=Community
        # url=serializers.HyperlinkedIdentityField(
        #     view_name='community',
        #     lookup_field='id'
        # )
        fields=('id','name', 'description', 'image','profile')
        depth=2

class Communities(ViewSet):
    
    def create(self, request):
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

        serializer = CommunitySerializer(community, context={'request':request})
        return Response(serializer.data, content_type='application/json')

    def retrieve(self, request, pk=None):
        try:
            community = Community.objects.get(pk=pk)
            serializer = CommunitySerializer(
                community,
                many=False,
                context={'request':request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        community = Community.objects.get(pk=pk)
        community.name = request.data['name'],
        community.description = request.data['description'],
        community.image = request.data['image']
        community.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            community = Community.objects.get(pk=pk)
            community.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Community.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        communities = Community.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            communities = communities.filter(name__startswith=name)
        serializer = CommunitySerializer(communities, many=True, context={'request':request})
        return Response(serializer.data)