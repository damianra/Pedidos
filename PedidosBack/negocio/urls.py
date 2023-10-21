from django.urls import path
from negocio.views import EmpresaRegister, VerEmpresa

urlpatterns = [
    path('registrar-empresa', EmpresaRegister.as_view()),
    path('ver-empresa', VerEmpresa.as_view()),
]