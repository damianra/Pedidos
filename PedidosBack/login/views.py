from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.sessions.models import Session
from datetime import datetime

from .serializadores import UserTokenSerializer
from rest_framework.views import APIView

# Create your views here.
class Login(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        log_serializer = self.serializer_class(data=request.data, context={'request':request})
        if log_serializer.is_valid():
            user = log_serializer.validated_data['user']
            token,created = Token.objects.get_or_create(user=user)
            user_serializado = UserTokenSerializer(user)
            if created:
                return Response({
                    'token': token.key,
                    'user': user_serializado.data,
                    'message': 'Inicio de Sesion exitoso.'
                }, status=status.HTTP_201_CREATED)
            else:
                '''
                ##
                ## BORRAR TOKEN Y SESION DE USUARIO
                ##
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()
                token = Token.objects.create(user=user)
                return Response({
                    'token': token.key,
                    'user': user_serializado.data,
                    'message': 'Inicio de Sesion exitoso.'
                }, status=status.HTTP_201_CREATED)
            print("Paso validacion")
            '''
                return Response({
                    'error': 'Ya se ha iniciado sesion,',
                    'token': token.key
                }, status = status.HTTP_409_CONFLICT)
        else:
            return Response({'mensaje':'Nombre de usuario o contraseña no incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        #return Response({'mensaje':'Respuesta'}, status=status.HTTP_200_OK)


class Logout(APIView):

    def get(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token')
            token = Token.objects.filter(key=token).first()
            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()

                session_message = 'Sesiones de usuario eliminadas'
                token_message = 'Token eliminado'
                return Response({'token_message':token_message, 'session_message':session_message},
                                    status=status.HTTP_200_OK)
            return Response({'error': 'No se ha encontrado el usuario con esas credenciales'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'No se recibio token'}, status=status.HTTP_409_CONFLICT)
