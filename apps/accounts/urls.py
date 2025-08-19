from django.urls import path

from .views import (
    CustomLoginView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    SellerRegisterView,
    UserMeEditView,
    UserMeView,
)

urlpatterns = [
    path("seller/registration/", SellerRegisterView.as_view(), name="seller-register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("me/", UserMeView.as_view(), name="profile"),
    path("edit/", UserMeEditView.as_view(), name="profile"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", CustomTokenVerifyView.as_view(), name="token-verify"),
]
