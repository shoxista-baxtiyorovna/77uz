from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = 20


class PagesPagination(CustomPagination):
    page_size = 10


class RegionPagination(CustomPagination):
    page_size = 5


class CategoryProductSearchPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
