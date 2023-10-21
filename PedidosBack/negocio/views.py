from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from negocio.models import Empresa
from negocio.serializers import EmpresaSerializer, VerEmpresaSerializer

import base64

# Create your views here.
class EmpresaRegister(APIView):
    def post(self, request,*args,**kwargs):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Empresa creada exitosamente.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class VerEmpresa(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
            codes = token.split('.')
            token_info = base64.b64decode(str(codes[1]+"=")).decode()
            user = User.objects.filter(id=eval(token_info)['user_id']).first()

            empr = Empresa.objects.filter(usuario=user).first()
        except:
            empr = None
        if empr:
            data = VerEmpresaSerializer(empr)
            return Response(data.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'El usuario no tiene una empresa registrada.'}, status=status.HTTP_400_BAD_REQUEST)