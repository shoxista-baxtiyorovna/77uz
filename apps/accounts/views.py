from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import CustomUser
from .serializers import SellerRegistrationSerializer


class SellerRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SellerRegistrationSerializer
    permission_classes = [AllowAny]
