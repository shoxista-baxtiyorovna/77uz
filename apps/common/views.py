from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Page, Region
from .serializers import PageListSerializer, PageDetailSerializer, RegionSerializer
from .pagination import PagesPagination, RegionPagination


class PageListView(ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer
    pagination_class = PagesPagination


class PageDetailView(RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer
    lookup_field = 'slug'


class RegionWithDistrictsView(ListAPIView):
    queryset = Region.objects.prefetch_related("districts").all()
    serializer_class = RegionSerializer
    pagination_class = RegionPagination
