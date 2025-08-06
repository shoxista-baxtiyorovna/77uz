from rest_framework import serializers


class PageListSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    title = serializers.CharField()


class PageDetailSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    title = serializers.CharField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class DistrictSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)


class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    districts = DistrictSerializer(many=True)