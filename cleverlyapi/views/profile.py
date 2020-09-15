from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.authtoken.models import Token

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from ..models import Profile

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # url = serializers.HyperlinkedIdentityField(
        #     view_name='profile',
        #     lookup_field='id'
        # )
        fields = ('id', 'user', 'profile_image', 'about', 'likes')
        depth = 1

class Profiles(ViewSet):
    
    def create(self, request):
        user = User.objects.create_user(
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            username=request.data['username'],
            password=request.data['password'],
            email=request.data['email']
        )

        profile = Profile.objects.create(
            about=request.data['about'],
            profile_image=request.data['profile_image'],
            user=user
        )

        token= Token.objects.create(user=user)

        data = json.dumps({"token":token.key})
        return HttpResponse(data, content_type='application/json')
    
    def retrieve(self, request, pk=None):
        """Handle GET requests
        Returns:
            Response -- JSON serialized profile instance
        """
        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(
                profile, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests
        Returns:
            Response -- Empty body with 204 status code
        """

        profile = Profile.objects.get(pk=pk)
        profile.profile_image = request.data["profile_image"]
        profile.about = request.data["about"]
        profile.save()

        user = User.objects.get(pk=profile.user_id)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):

        if request.user.id:
            profiles = Profile.objects.filter(user=request.user.id)
        else:
            profiles = Profile.objects.all()
        serializer = ProfileSerializer(
            profiles,
            many=True,
            context={'request':request}
        )
        return Response(serializer.data)
