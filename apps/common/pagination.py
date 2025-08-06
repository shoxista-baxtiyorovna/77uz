from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = 20


class PagesPagination(CustomPagination):
    page_size = 10


class RegionPagination(CustomPagination):
    page_size = 5
