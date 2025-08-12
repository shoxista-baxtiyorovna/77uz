from django.urls import path

from .views import SellerRegisterView

urlpatterns = [
    path("seller/registration/", SellerRegisterView.as_view(), name="seller-register"),
]
