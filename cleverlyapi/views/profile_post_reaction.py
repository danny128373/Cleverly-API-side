from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Profile
from ..models import Post
from ..models import ProfilePostReaction as ProfilePostReactionModel


class ProfilePostReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for profilepostreactions"""

    class Meta:
        model = ProfilePostReactionModel
        fields = ('id', 'profile', 'post', 'status')
        depth = 2


class ProfilePostReaction(ViewSet):

    def create(self, request):
        """
        Handle POST request for a profilepostreaction
        Returns: JSON serialized profilepostreaction instance
        """
        profile = Profile.objects.get(user_id=request.auth.user)
        post = Post.objects.get(pk=request.data['post_id'])

        profile_post_reaction = ProfilePostReactionModel.objects.create(
            status=request.data['status'],
            profile=profile,
            post=post
        )

        serializer = ProfilePostReactionSerializer(
            profile_post_reaction, context={'request': request})
        return Response(serializer.data, content_type='application/json')

    def update(self, request, pk=None):
        """
        Handling a PUT request for a profilepostreaction
        Returns: Empty body with 204 status code
        """
        profile_post_reaction = ProfilePostReactionModel.objects.get(
            pk=request.data['id'])
        profile_post_reaction.status = request.data['status']
        profile_post_reaction.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single profilepostreaction
        Returns: JSON serialized profilepostreaction instance
        """
        try:
            profile_post_reaction = ProfilePostReactionModel.objects.get(pk=pk)
            serializer = ProfilePostReactionSerializer(
                profile_post_reaction,
                many=False,
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handles DELETE requests for single profilepostreaction"""
        try:
            profile_post_reaction = ProfilePostReactionModel.objects.get(pk=pk)
            profile_post_reaction.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProfilePostReactionModel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """
        Handle GET requests for profilepostreactions
        Returns: Response JSON serialized list of profilepostreactions
        """
        profile_post_reaction = ProfilePostReactionModel.objects.all()
        serializer = ProfilePostReactionSerializer(
            profile_post_reaction,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)
