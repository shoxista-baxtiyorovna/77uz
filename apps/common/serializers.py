from rest_framework import serializers


class PageListSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    title = serializers.CharField()


class PageDetailSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    title = serializers.CharField()
    content = serializers.CharField()
    created_time = serializers.DateTimeField()
    updated_time = serializers.DateTimeField()


class DistrictSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)


class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    districts = DistrictSerializer(many=True)


class SettingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    phone = serializers.CharField(max_length=20)
    support_email = serializers.EmailField()
    working_hours = serializers.CharField(max_length=100)
    app_version = serializers.CharField(max_length=50)
    maintenance_mode = serializers.BooleanField(default=False)
