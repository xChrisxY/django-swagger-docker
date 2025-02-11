from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializer import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
@api_view(['POST'])
def register(request):

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():

        user = serializer.save()

        user.set_password(serializer.validated_data["password"])
        user.save()

        #token = Token.objects.create(user=user)
        return Response({"message": "User created successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):

    user = get_object_or_404(User, username=request.data['username'])

    if not user.check_password(request.data['password']): 
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

    #token, created = Token.objects.get_or_create(user=user)
    refresh = RefreshToken.for_user(user)
    serializer = UserSerializer(instance=user)

    return Response({"refresh": str(refresh), "access": str(refresh.access_token), "user": serializer.data}, status=status.HTTP_200_OK)


    
