from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from cleverlyapi.models import *
from cleverlyapi.views import register_user
from cleverlyapi.views import login_user
from cleverlyapi.views import Comments
from cleverlyapi.views import Communities
from cleverlyapi.views import Conversations
from cleverlyapi.views import Messages
from cleverlyapi.views import Posts
from cleverlyapi.views import Profiles
from cleverlyapi.views import ProfileCommunities

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'comments', Comments, 'comment')
router.register(r'communities', Communities, 'community')
router.register(r'conversations', Conversations, 'conversation')
router.register(r'messages', Messages, 'message')
router.register(r'posts', Posts, 'post')
router.register(r'profiles', Profiles, 'profile')
router.register(r'profilecommunities', ProfileCommunities, 'profilecommunity')


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', register_user),
    path('login/', login_user),
]
