from django.contrib.auth import login
import json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from ..models import Profile


@csrf_exempt
def login_user(request):
    """Handles request for login a user in"""
    req_body = json.loads(request.body.decode())

    if request.method == 'POST':
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    """Handles request for registering the user"""
    req_body = json.loads(request.body.decode())

    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )

    new_profile = Profile.objects.create(
        about=req_body['about'],
        profile_image=req_body['profile_image'],
        likes=req_body['likes'],
        user=new_user
    )

    token = Token.objects.create(user=new_user)
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json')
