from common.utils.custom_response_decorator import custom_response
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from .models import CustomUser
from .serializers import (
    CustomLoginSerializer,
    CustomTokenRefreshSerializer,
    CustomTokenVerifySerializer,
    SellerRegistrationSerializer,
    UserMeSerializer,
)


@extend_schema(tags=["Accounts"], description="Foydalanuvchini ro‘yxatdan o‘tkazish")
@custom_response
class SellerRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SellerRegistrationSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=["Accounts"], description="Foydalanuvchining o'z profilini olish")
@custom_response
class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["Accounts"], description="Foydalanuvchining ma'lumotlarini yangilash")
@custom_response
class UserMeEditView(generics.UpdateAPIView):
    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["Accounts"], description="Foydalanuvchini autentifikatsiya qilish")
@custom_response
class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@extend_schema(tags=["Accounts"], description="Access tokenni yangilash")
@custom_response
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


@extend_schema(tags=["Accounts"], description="Tokenni tekshirish va uning haqiqiyligini aniqlash")
@custom_response
class CustomTokenVerifyView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = CustomTokenVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
