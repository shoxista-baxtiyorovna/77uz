from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class PhotoMixin(serializers.Serializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        main = getattr(obj, "photos", None)
        if main:
            main_photo = main.filter(is_main=True).first()
            if main_photo:
                request = self.context.get("request")
                return (
                    request.build_absolute_uri(main_photo.image.url)
                    if request
                    else main_photo.image.url
                )
        return None


class LikedMixin(serializers.Serializer):
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        device_id = None

        if request:
            device_id = request.query_params.get("device_id") or request.data.get("device_id")

        if user and user.is_authenticated:
            return obj.favourited_by.filter(user=user).exists()
        elif device_id:
            return obj.favourited_by.filter(device_id=device_id).exists()
        return False


class UserOrDeviceMixin(serializers.Serializer):

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if user and user.is_authenticated:
            attrs["user"] = user
            attrs.pop("device_id", None)
        else:
            device_id = request.data.get("device_id")  # attrs.get('device_id') o‘rniga
            if not device_id:
                raise ValidationError("Unauthenticated users must provide a device_id.")
        return attrs


class ViewCountMixin:
    def increase_view_count(self, obj):
        obj.view_count = obj.view_count + 1
        obj.save(update_fields=["view_count"])
