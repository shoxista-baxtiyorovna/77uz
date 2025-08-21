from common.models import Region
from rest_framework import serializers

from .mixins import LikedMixin, PhotoMixin, UserOrDeviceMixin
from .models import Ad, AdImage, Category, FavouriteProduct, SearchHistory


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.URLField()
    product_count = serializers.IntegerField()  # string sifatida JSON responsedagi kabi


class SubCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.URLField()


class CategoryWithChildrenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.URLField()
    children = SubCategorySerializer(many=True)


class AdImageSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all(), source="ad")

    class Meta:
        model = AdImage
        fields = ["id", "image", "is_main", "product_id", "created_time"]
        read_only_fields = ["id", "created_time"]


class SellerInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    phone_number = serializers.CharField()
    profile_photo = serializers.SerializerMethodField()

    def get_profile_photo(self, obj):
        request = self.context.get("request")
        if obj.profile_photo:
            return (
                request.build_absolute_uri(obj.profile_photo.url)
                if request
                else obj.profile_photo.url
            )
        return None


class AdListSerializer(LikedMixin, PhotoMixin, serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    price = serializers.DecimalField(max_digits=14, decimal_places=2)
    created_time = serializers.DateTimeField()
    address = serializers.CharField(source="seller.address.name")
    seller = SellerInfoSerializer(read_only=True)
    updated_time = serializers.DateTimeField()


class AdCreateSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False)
    seller = SellerInfoSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = [
            "name",
            "description",
            "price",
            "status",
            "category",
            "seller",
            "address",
            "photos",
        ]

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        photos_data = validated_data.pop("photos", [])
        user = validated_data.pop("seller", None)
        ad = Ad.objects.create(seller=user, **validated_data)

        ad_photos = []
        for idx, img in enumerate(photos_data):
            ad_photos.append(AdImage(ad=ad, image=img, is_main=(idx == 0)))
        AdImage.objects.bulk_create(ad_photos)

        return ad


class AdDetailSerializer(LikedMixin, PhotoMixin, serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=14, decimal_places=2)
    created_time = serializers.DateTimeField()
    address = serializers.CharField(source="seller.address.name")
    seller = SellerInfoSerializer(read_only=True)
    updated_time = serializers.DateTimeField()


class FavouriteProductSerializer(UserOrDeviceMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_time = serializers.DateTimeField(read_only=True)
    device_id = serializers.CharField(required=False)

    class Meta:
        model = FavouriteProduct
        fields = ["id", "product", "device_id", "created_time"]

    def get_device_id(self, obj):
        if obj.user is None:
            return obj.device_id
        return None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.user is not None:
            rep.pop("device_id", None)
        return rep

    def create(self, validated_data):
        user = validated_data.get("user")
        device_id = validated_data.get("device_id")
        product = validated_data["product"]

        favourite, _ = FavouriteProduct.objects.get_or_create(
            user=user, device_id=device_id, product=product
        )
        return favourite


class MyFavouriteProductListSerializer(LikedMixin, PhotoMixin, serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=14, decimal_places=2)
    created_time = serializers.DateTimeField()
    address = serializers.CharField(source="seller.address.name")
    seller = serializers.CharField(source="seller.full_name")
    updated_time = serializers.DateTimeField()


class MyAdListSerializer(LikedMixin, PhotoMixin, serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    created_time = serializers.DateTimeField(read_only=True)
    address = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    updated_time = serializers.DateTimeField(read_only=True)


class MyAdDetailSerializer(serializers.ModelSerializer):
    new_photos = serializers.ListField(
        child=serializers.URLField(), write_only=True, required=False
    )
    photos = serializers.SerializerMethodField()
    published_at = serializers.DateTimeField(source="created_time", read_only=True)

    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "category",
            "price",
            "new_photos",
            "photos",
            "published_at",
            "status",
            "view_count",
            "updated_time",
        ]
        read_only_fields = [
            "id",
            "slug",
            "photos",
            "published_at",
            "status",
            "view_count",
            "updated_time",
        ]

    def get_photos(self, obj):
        request = self.context.get("request")
        photos = obj.photos.all()
        return [request.build_absolute_uri(photo.image.url) for photo in photos]

    def update(self, instance, validated_data):
        new_photos = validated_data.pop("new_photos", None)
        if new_photos:
            for url in new_photos:
                AdImage.objects.create(ad=instance, image=url)

        return super().update(instance, validated_data)


class SearchHistorySerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    region_id = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    search_query = serializers.CharField(source="query")

    class Meta:
        model = SearchHistory
        fields = [
            "id",
            "category",
            "search_query",
            "price_min",
            "price_max",
            "region_id",
            "created_time",
        ]
        read_only_fields = ["id", "created_time"]

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user if request and request.user.is_authenticated else None
        device_id = request.data.get("device_id") or request.query_params.get("device_id")

        if not user and not device_id:
            raise serializers.ValidationError("Token yoki device_id majburiy.")

        attrs["user"] = user
        attrs["device_id"] = device_id
        return attrs


class CountIncreaseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  # ad.id
    category = serializers.IntegerField(source="category.id")  # ad.category.id
    search_count = serializers.IntegerField(read_only=True)
    updated_time = serializers.DateTimeField(read_only=True)


class PopularSearchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source="product.name", read_only=True)
    icon = serializers.SerializerMethodField()
    search_count = serializers.IntegerField(read_only=True)

    def get_icon(self, obj):
        if obj.product.category and getattr(obj.product.category, "icon", None):
            return obj.product.category.icon.url
        return ""


class CategoryProductUnionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    def get_type(self, obj):
        if hasattr(obj, "icon"):  # Category object
            return "category"
        return "product"

    def get_icon(self, obj):
        if hasattr(obj, "icon"):  # Category
            return obj.icon.url if obj.icon else ""
        return obj.category.icon.url if getattr(obj, "category", None) and obj.category.icon else ""
