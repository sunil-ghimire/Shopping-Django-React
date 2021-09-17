import random
from django.contrib.auth.backends import UserModel
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from api.user.serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import re

# Create your views here.
def generate_session_token(length=10):   
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in range(length))

@csrf_exempt
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error':'Send a post request with valid parameter'})

    username = request.POST['email']
    password = request.POST['password']


# validation part
    if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", username):
        return JsonResponse({'error':'Enter a valid email'})

    if len(password) < 3:
        return JsonResponse({"error":'Password needs to be atleast of 3 char'})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)
        if user.check_password(password):
            user_dict = UserModel.objects.filter(email=username).values().first()
            user_dict.pop('password')

            if user.session_token != "0":
                user.session_token = "0"
                user.save()
                return JsonResponse({'error':'Previous session exists!'})

            token = str(generate_session_token())
            user.session_token = token
            user.save()
            login(request, user)
            return JsonResponse({'token':token, 'user':user_dict})
        else:
            return JsonResponse({"error":"Invalid Password!"})


    except UserModel.DoesNotExist:
        return JsonResponse({'error':'invalid Email'})


def signout(request, id):
    logout(request)

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = "0"
        user.save()
    except UserModel.DoesNotExist:
        return JsonResponse({"error":"Invalid User ID"})
    
    return JsonResponse({"success":'Logout Success!'})



class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create':[AllowAny]}

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]