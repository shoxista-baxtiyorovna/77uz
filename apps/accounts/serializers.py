from rest_framework import serializers

from .models import Address, Category, CustomUser


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["name", "lat", "long"]


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
