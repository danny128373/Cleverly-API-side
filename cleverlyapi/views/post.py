from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Profile
from ..models import Community
from ..models import Post
from ..models import ProfileCommunity


class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""

    class Meta:
        model = Post
        fields = ('id', 'created_at', 'community',
                  'profile', 'content', 'title')
        depth = 2


class Posts(ViewSet):

    def create(self, request):
        """
        Handle POST request for a post
        Returns: JSON serialized post instance
        """
        profile = Profile.objects.get(pk=request.data['profile_id'])
        community = Community.objects.get(pk=request.data['community_id'])

        post = Post.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            community=community,
            profile=profile
        )
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, content_type='application/json')

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single post
        Returns: JSON serialized post instance
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(
                post,
                many=False,
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        Handling a PUT request for a post
        Returns: Empty body with 204 status code
        """
        post = Post.objects.get(pk=pk)
        post.title = request.data['title']
        post.content = request.data['content']
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handles DELETE requests for single post"""
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """
        Handle GET requests for posts
        Returns: Response JSON serialized list of posts of communities the user is following
        """
        profile = Profile.objects.get(user_id=request.auth.user)
        posts = Post.objects.all()
        communities = ProfileCommunity.objects.filter(profile_id=profile.id)
        community_ids = []
        post_list = []
        for community in communities:
            community_ids.append(community.community_id)

        for post in posts:
            for community_id in community_ids:
                if post.community_id == community_id:
                    post_list.append(post)

        serializer = PostSerializer(
            post_list,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
