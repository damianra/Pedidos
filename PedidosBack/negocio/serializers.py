from rest_framework import serializers
from negocio.models import Empresa, RedesSociales
from django.contrib.auth.models import User

import base64

class EmpresaSerializer(serializers.Serializer):
    token = serializers.CharField()
    nombre_empresa = serializers.CharField()
    telefono = serializers.CharField()
    delivery = serializers.BooleanField()
    activo = serializers.BooleanField()
    horarios = serializers.JSONField()

    whatsapp = serializers.CharField()
    faceboock = serializers.CharField()
    instagram = serializers.CharField()

    def create(self, validated_data):
        codes = validated_data.get('token').split(' ')[0].split('.')
        token_info = base64.b64decode(str(codes[1]+"=")).decode()
        user = User.objects.filter(id=eval(token_info)['user_id']).first()

        instance = Empresa()
        instance.usuario = user
        instance.nombre_empresa = validated_data.get('nombre_empresa')
        instance.telefono = validated_data.get('telefono')
        instance.delivery = validated_data.get('delivery')
        instance.activo = validated_data.get('activo')
        instance.horarios = validated_data.get('horarios')

        redes = RedesSociales()
        redes.whatsapp = validated_data.get('whatsapp')
        redes.faceboock = validated_data.get('faceboock')
        redes.instagram = validated_data.get('instagram')

        redes.save()

        instance.redes_sociales = redes
        instance.save()
        return instance
    
    def validate_empresa(self, data):
        emp = Empresa.objects.filter(nombre_empresa=data.get('nombre_empresa'))
        if len(emp) != 0:
            raise serializers.ValidationError("La empresa ya existe.")
        else:
            return data


class VerEmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'