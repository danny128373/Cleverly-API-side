from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Profile
from ..models import Community

class CommunitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=Community
        url=serializers.HyperlinkedIdentityField(
            view_name='community',
            lookup_field='id'
        )
        fields=('id','url','name', 'description', 'image','profile')
        depth=2

class Communities(ViewSet):
    
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized community instance
        """
        profile = Profile.objects.get(user_id=request.user.id)
        community = Community.objects.create(
            name=request.data['name'],
            description=request.data['description'],
            image=request.data['image'],
            profile=profile
        )
        serializer = CommunitySerializer(community, context={'request':request})
        return Response(serializer.data, content_type='application/json')

    def retrieve(self, request, pk=None):
       """Handle GET operation
        Returns:
            Response -- JSON serialized community instance
        """   
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
        """Handle PUT requests for communities
        Returns:
            Response -- Empty body with 204 status code
        """
        community = Community.objects.get(pk=pk)
        community.name = request.data['name'],
        community.description = request.data['description'],
        community.image = request.data['image']
        community.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a community
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            community = Community.objects.get(pk=pk)
            community.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Community.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
         """Handle GET requests to community resource
        Returns:
            Response -- JSON serialized list of products
        """
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True, context={'request':request})
        return Response(serializer.data)