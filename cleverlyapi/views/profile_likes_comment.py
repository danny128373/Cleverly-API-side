from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Profile
from ..models import Comment
from ..models import ProfileLikesComment as ProfileLikesCommentModel


class ProfileLikesCommentSerializer(serializers.ModelSerializer):
    """JSON serializer for profilelikescomment"""

    class Meta:
        model = ProfileLikesCommentModel
        fields = ('id', 'profile', 'comment', 'status')
        depth = 2


class ProfileLikesComment(ViewSet):

    def create(self, request):
        """
        Handle POST request for a profilelikescomment
        Returns: JSON serialized profilelikescomment instance
        """
        profile = Profile.objects.get(user_id=request.auth.user)
        comment = Comment.objects.get(pk=request.data['comment_id'])

        profile_likes_comment = ProfileLikesCommentModel.objects.create(
            status=request.data['status'],
            profile=profile,
            comment=comment
        )
        serializer = ProfileLikesCommentSerializer(
            profile_likes_comment, context={'request': request})
        return Response(serializer.data, content_type='application/json')

    def update(self, request, pk=None):
        """
        Handling a PUT request for a profilelikescomment
        Returns: Empty body with 204 status code
        """
        profile_likes_comment = ProfileLikesCommentModel.objects.get(
            pk=request.data['id'])
        profile_likes_comment.status = request.data['status']
        profile_likes_comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        """
        Handle GET requests for single profilelikescomment
        Returns: JSON serialized profilelikescomment instance
        """
        try:
            profile_likes_comment = ProfileLikesCommentModel.objects.get(pk=pk)
            serializer = ProfileLikesCommentSerializer(
                profile_likes_comment,
                many=False,
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handles DELETE requests for single profilelikescomment"""

        try:
            profile_likes_comment = ProfileLikesCommentModel.objects.get(pk=pk)
            profile_likes_comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProfileLikesCommentModel.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """
        Handle GET requests for profilelikescomments
        Returns: Response JSON serialized list of profilelikescomments
        """
        profile_likes_comment = ProfileLikesCommentModel.objects.all()
        serializer = ProfileLikesCommentSerializer(
            profile_likes_comment,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)
