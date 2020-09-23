from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Profile
from ..models import Post
from ..models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""

    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'profile')
        depth = 2


class Comments(ViewSet):

    def create(self, request):
        """
        Handle POST request for a comment
        Returns: JSON serialized comment instance
        """
        profile = Profile.objects.get(pk=request.data['profile_id'])
        post = Post.objects.get(pk=request.data['post_id'])

        comment = Comment.objects.create(
            content=request.data['content'],
            profile=profile,
            post=post
        )

        serializer = CommentSerializer(comment, context={'request': request})

        return Response(serializer.data, content_type='application/json')

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single comment
        Returns: JSON serialized comment instance
        """
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(
                comment,
                many=False,
                content={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        Handling a PUT request for a comment
        Returns: Empty body with 204 status code
        """
        comment = Comment.objects.get(pk=request.data['id'])
        comment.content = request.data['content']
        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handles DELETE requests for single comment"""
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """
        Handle GET requests for comments
        Returns: Response JSON serialized list of comments
        """
        comments = Comment.objects.all()
        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)
