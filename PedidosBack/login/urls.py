from django.urls import path
from .views import Login, Logout

urlpatterns = [
    path('', Login.as_view()),
    path('/logout', Logout.as_view()),
]