from django_filters import rest_framework as filters

from .models import Ad


class AdFilter(filters.FilterSet):
    price__gte = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price__lte = filters.NumberFilter(field_name="price", lookup_expr="lte")
    category_ids = filters.BaseInFilter(field_name="category_id", lookup_expr="in")
    is_top = filters.BooleanFilter(field_name="is_top")
    seller_id = filters.NumberFilter(field_name="seller_id")
    district_id = filters.NumberFilter(field_name="address__district_id")
    region_id = filters.NumberFilter(field_name="address__region_id")

    class Meta:
        model = Ad
        fields = []
