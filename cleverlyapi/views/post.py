from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Profile
from ..models import Community
from ..models import Post

class PostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Post
        url = serializers.HyperlinkedIdentityField(
            view_name='post',
            lookup_field='id'
        )
        fields=('id','url', 'post_date', 'community', 'profile', 'content', 'title', 'likes')
        depth=2

class Posts(ViewSet):

    def create(self,request):
        profile= Profile.objects.get(user_id=request.user.id)
        community = Community.objects.get(pk=request.data['community_id'])

        post = Post.objects.create(
            title=request.data["title"],
            content=request.data["content"],
            community = community,
            profile = profile
        )
        serializer = PostSerializer(post, context={'request':request})
        return Response(serializer.data, content_type='application/json')

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(
                post,
                many=False,
                context={'request':request}
            )
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def update(self, request, pk=None):

        post = Post.objects.get(pk=pk)
        post.title = request.data['title'],
        post.content = request.data['content']
        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts,
            many=True,
            context={'request':request}
        )
        return Response(serializer.data)

