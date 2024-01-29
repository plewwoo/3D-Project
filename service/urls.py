from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()

urlpatterns = [
    path('register/', Register.as_view(), name='auth-register'),
    path('login/', Login.as_view(), name='auth-login'),
    path('check-login/', CheckLogin.as_view(), name='auth-check-login'),
    path('profile/<int:id>/', UserProfile.as_view(), name='user'),
    path('models/<int:id>/', UploadFile.as_view(), name='models'),
    path('upload/', UploadFile.as_view(), name='upload'),
    path('model/<int:id>', GetModel.as_view(), name='model')
    # path('login/', MyObtainTokenPairView.as_view(), name='auth-login'),
]

urlpatterns += router.urls