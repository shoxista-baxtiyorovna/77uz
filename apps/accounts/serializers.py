from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from store.models import Category

from .models import Address, CustomUser

User = get_user_model()


class AddressSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    lat = serializers.FloatField()
    long = serializers.FloatField()


class SellerRegistrationSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    category_id = serializers.IntegerField(source="category.id", read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "full_name",
            "project_name",
            "category_id",
            "phone_number",
            "category",
            "address",
            "status",
        ]

    def create(self, validated_data):
        address_data = validated_data.pop("address")
        category = validated_data.pop("category")

        address = Address.objects.create(**address_data)

        user = CustomUser.objects.create(
            **validated_data,
            category=category,
            address=address,
            is_active=False,
            role=CustomUser.Roles.SELLER,
            status=CustomUser.Status.PENDING,
        )
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["address"] = instance.address.name if instance.address else None
        return data


class UserMeSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "phone_number",
            "profile_photo",
            "address",
        ]


class CustomLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid phone number or password.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid phone number or password.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        refresh = RefreshToken.for_user(user)

        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": {
                "id": user.id,
                "full_name": getattr(user, "full_name", ""),
                "phone_number": user.phone_number,
            },
        }


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return {"access_token": data["access"]}


class CustomTokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        token_str = attrs.get("token")

        try:
            token = UntypedToken(token_str)
            payload = token.payload

            return {"valid": True, "user_id": payload.get("user_id")}
        except (InvalidToken, TokenError):
            raise serializers.ValidationError({"detail": "Token noto‘g‘ri yoki muddati tugagan"})
