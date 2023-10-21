from django.urls import path
from .views import Login, Logout, RegisterUser
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('', Login.as_view()),
    path('logout', Logout.as_view()),
    path('refresh', jwt_views.TokenRefreshView.as_view()),
    path('register', RegisterUser.as_view()),
    #path('logout', TokenBlacklistView.as_view(), name='token_blacklist'),
]