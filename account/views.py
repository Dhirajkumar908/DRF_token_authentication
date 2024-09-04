from django.shortcuts import render, HttpResponse
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

#serilaizer
from .serializers import *

# Create your views here.
class UserloginAPIview(APIView):
    def post(self, request, *args, **kwargs):
        """
        This post api for user login
        """
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response={
                "username":{
                    "detail":"User dose not exist"
                }
            }
            if User.objects.filter(username=request.data['username']).exists():
                user=User.objects.get(username=request.data["username"])
                token, created= Token.objects.get_or_create(user=user)
                response={
                    "success":True,
                    "username":user.username,
                    "email":user.email,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    'token':token.key,
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer=UserRagistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user=User.objects.get(username=serializer.data['username'])
            response={
                'message':'Success',
                'user':serializer.data,
                'Token':Token.objects.get(user=user).key
            }
            return Response(response, status=status.HTTP_200_OK)
        raise ValidationError(serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)


class UserLogoutAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request, *args):
        token=Token.objects.get(user=request.user)
        token.delete()
        return Response({"success":True, "details":" logout out!"}, status=status.HTTP_200_OK)