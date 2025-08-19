from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Page, Region, Setting
from .pagination import PagesPagination, RegionPagination
from .serializers import (
    PageDetailSerializer,
    PageListSerializer,
    RegionSerializer,
    SettingSerializer,
)
from .utils.custom_response_decorator import custom_response


@extend_schema(tags=["Common"], description="Statik sahifalar ro'yxatini olish")
@custom_response
class PageListView(ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer
    pagination_class = PagesPagination


@extend_schema(tags=["Common"], description="Ma'lum slug bo'yicha statik sahifani olish")
@custom_response
class PageDetailView(RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    lookup_field = "slug"


@extend_schema(tags=["Common"], description="Viloyatlar va ularning tumanlarini ro'yxatini olish")
@custom_response
class RegionWithDistrictsView(ListAPIView):
    queryset = Region.objects.prefetch_related("districts").all()
    serializer_class = RegionSerializer
    pagination_class = RegionPagination


@extend_schema(tags=["Common"], description="Ilova sozlamalarini olish")
@custom_response
class SettingRetrieveView(RetrieveAPIView):
    serializer_class = SettingSerializer

    def get_object(self):
        return Setting.objects.first()
