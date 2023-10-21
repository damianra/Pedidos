from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from login.serializadores import ObtenerToken, UserSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


import base64

class Login(TokenObtainPairView):
    serializer_class = ObtenerToken

    def post(self,request,*args,**kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(
            username=username,
            password=password,
        )

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer =  UserLoginSerializer(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de sesion exitoso'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Usuario o contraseña incorrectos.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Usuario o contraseña incorrectos.'}, status=status.HTTP_400_BAD_REQUEST)
    

class Logout(GenericAPIView):
    def post(self,request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        codes = token.split('.')
        token_info = base64.b64decode(str(codes[1]+"=")).decode()
       
        user = User.objects.filter(id=eval(token_info)['user_id'])
        if user.exists():
            RefreshToken.for_user(user=user.first())
            return Response({'message':'Ha cerrado sesion exitosamente'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe usuario'}, status=status.HTTP_400_BAD_REQUEST)
    

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Usuario creado exitosamente.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)