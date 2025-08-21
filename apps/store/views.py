from common.pagination import StandardResultsSetPagination
from common.utils.custom_response_decorator import custom_response
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, generics, permissions, serializers, status
from rest_framework.response import Response

from .filters import AdFilter
from .mixins import ViewCountMixin
from .models import Ad, AdImage, Category, FavouriteProduct, SearchCount, SearchHistory
from .serializers import (
    AdCreateSerializer,
    AdDetailSerializer,
    AdImageSerializer,
    AdListSerializer,
    CategoryProductUnionSerializer,
    CategorySerializer,
    CategoryWithChildrenSerializer,
    CountIncreaseSerializer,
    FavouriteProductSerializer,
    MyAdDetailSerializer,
    MyAdListSerializer,
    MyFavouriteProductListSerializer,
    SearchHistorySerializer,
    SubCategorySerializer,
)


@extend_schema(tags=["Store"], description="Kategoriyalar ro‘yxatini olish")
@custom_response
class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True).annotate(
            product_count=Count("products")
        )


@extend_schema(tags=["Store"], description="Kategoriyalar va sub-kategoriyalar ro‘yxatini olish")
@custom_response
class CategoryWithChildrenView(generics.ListAPIView):
    serializer_class = CategoryWithChildrenSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Category.objects.prefetch_related("children")


@extend_schema(tags=["Store"], description="Sub-kategoriyalarni ro‘yxatini olish")
@custom_response
class SubCategoryListView(generics.ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        return Category.objects.filter(parent__isnull=False).annotate(
            product_count=Count("products")
        )


@extend_schema(tags=["Store"], description="E'lonlar ro‘yxatini olish")
@custom_response
class AdListView(generics.ListAPIView):
    serializer_class = AdListSerializer
    queryset = Ad.objects.filter(status=Ad.Status.ACTIVE)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AdFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_time", "view_count"]
    ordering = ["-created_time"]


@extend_schema(tags=["Store"], description="Yangi e'lon yaratish")
@custom_response
class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        ad_instance = serializer.instance
        detail_serializer = AdDetailSerializer(ad_instance, context={"request": request})
        return Response(detail_serializer.data, status=201, headers=headers)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


@extend_schema(tags=["Store"], description="Bitta e'lonni olish")
@custom_response
class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    lookup_field = "slug"


@extend_schema(tags=["Store"], description="Mahsulotni sevimlilarga qo'shish")
@custom_response
class FavouriteProductCreateView(generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["Store"], description="Mahsulotni device_id orqali sevimlilarga qo'shish")
@custom_response
class FavouriteProductCreateByIDView(generics.CreateAPIView):
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        device_id = self.request.data.get("device_id")
        if not device_id:
            raise serializers.ValidationError({"device_id": "This field is required."})
        serializer.save(device_id=device_id)


@extend_schema(tags=["Store"], description="Mahsulotni sevimlilardan olib tashlash")
@custom_response
class FavouriteProductDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "product_id"

    def get_queryset(self):
        return FavouriteProduct.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get(self.lookup_url_kwarg)
        favourite = self.get_queryset().filter(product_id=product_id).first()
        if not favourite:
            return Response({"detail": "Favourite not found."}, status=status.HTTP_404_NOT_FOUND)
        favourite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Store"], description="Mahsulotni device_id orqali sevimlilardan olib tashlash"
)
@custom_response
class FavouriteProductDeleteByDeviceView(generics.DestroyAPIView):
    permission_classes = [permissions.AllowAny]
    lookup_url_kwarg = "product_id"

    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get(self.lookup_url_kwarg)
        device_id = request.data.get("device_id") or request.query_params.get("device_id")
        if not device_id:
            return Response(
                {"device_id": "This field is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        favourite = FavouriteProduct.objects.filter(
            product_id=product_id, device_id=device_id
        ).first()
        if not favourite:
            return Response({"detail": "Favourite not found."}, status=status.HTTP_404_NOT_FOUND)

        favourite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Store"], description="Joriy foydalanuvchining sevimli mahsulotlarimni olish")
@custom_response
class MyFavouriteProductListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MyFavouriteProductListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Ad.objects.filter(favourited_by__user=self.request.user).distinct()


@extend_schema(
    tags=["Store"],
    description="Joriy foydalanuvchining sevimli mahsulotlarimni device_id orqali olish",
)
@custom_response
class MyFavouriteProductByIDListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyFavouriteProductListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        device_id = self.request.query_params.get("device_id")
        user = self.request.user if self.request.user.is_authenticated else None

        if user:
            return Ad.objects.filter(favourited_by__user=user).distinct()
        elif device_id:
            return Ad.objects.filter(favourited_by__device_id=device_id).distinct()
        return Ad.objects.none()

    def list(self, request, *args, **kwargs):
        device_id = request.query_params.get("device_id")
        if not device_id:
            return Response(
                {"device_id": "This field is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Store"], description="Joriy foydalanuvchining e'lonlarini olish")
@custom_response
class MyAdListView(generics.ListAPIView):
    serializer_class = MyAdListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Ad.objects.filter(seller=self.request.user)


@extend_schema_view(
    get=extend_schema(tags=["Store"], description="Mahsulot ma'lumotlarini olish"),
    put=extend_schema(tags=["Store"], description="Mahsulot ma'lumotlarini yangilash"),
    patch=extend_schema(tags=["Store"], description="Mahsulot ma'lumotlarini qisman yangilash"),
    delete=extend_schema(tags=["Store"], description="Mahsulotni o'chirish"),
)
@custom_response
class MyAdDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MyAdDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ad.objects.filter(seller=self.request.user)


@extend_schema(tags=["Store"], description="Mahsulotni yuklab olish va view countni oshirish")
@custom_response
class ProductDownloadView(ViewCountMixin, generics.RetrieveAPIView):
    queryset = Ad.objects.select_related("seller", "category").prefetch_related("photos")
    serializer_class = AdDetailSerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.increase_view_count(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(tags=["Store"], description="E'lon uchun yangi rasm yaratish")
@custom_response
class AdImageCreateView(generics.CreateAPIView):
    queryset = AdImage.objects.all()
    serializer_class = AdImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


"""

@extend_schema_view(

    get=extend_schema(
        tags=["Store"],
        description="Bitta rasmni olish"
    ),
    put=extend_schema(
        tags=["Store"],
        description="Bitta rasmni to‘liq yangilash"
    ),
    patch=extend_schema(
        tags=["Store"],
        description="Bitta rasmni qisman yangilash"
    ),
    delete=extend_schema(
        tags=["Store"],
        description="Bitta rasmni o‘chirish"
    ),
)
@custom_response
class AdPhotoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdImage.objects.all()
    serializer_class = AdImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
"""


@extend_schema(tags=["Store"], description="E'lonni qidirish va saralash")
@custom_response
class AdSearchView(generics.ListAPIView):
    serializer_class = CategoryProductUnionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "created_time"]
    ordering = ["-created_time"]  # default sort

    def get_queryset(self):
        queryset = Ad.objects.all()
        query = self.request.query_params.get("q")

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(category__name__icontains=query)
            )
        return queryset


@extend_schema(tags=["Store"], description="Foydalanuvchining qidiruv tarixini yaratish")
@custom_response
class MySearchCreateView(generics.CreateAPIView):
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)


@extend_schema(
    tags=["Store"],
    description="Foydalanuvchi yoki device bo‘yicha saqlangan qidiruv tarixini ro‘yxatlash",
)
@custom_response
class MySearchListView(generics.ListAPIView):
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return SearchHistory.objects.for_request(self.request)


@extend_schema(
    tags=["Store"],
    description="Foydalanuvchi yoki device bo‘yicha saqlangan qidiruv tarixidan "
    "ma'lum bir qidiruvni o'chirish",
)
@custom_response
class MySearchDeleteView(generics.DestroyAPIView):
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "id"

    def get_queryset(self):
        return SearchHistory.objects.for_request(self.request)


@extend_schema(
    tags=["Store"],
    description="Kategoriya yoki mahsulot uchun qidiruv sonini oshiradi"
    " va view_count ni yangilaydi.",
)
@custom_response
class CountIncreaseView(generics.RetrieveAPIView):
    serializer_class = CountIncreaseSerializer
    queryset = Ad.objects.all()
    lookup_field = "id"

    def get_object(self):
        ad_id = self.kwargs.get("id")
        ad = get_object_or_404(Ad, id=ad_id)

        search_count, created = SearchCount.objects.get_or_create(product=ad)
        search_count.search_count += 1
        search_count.save()

        ad.view_count += 1
        ad.save(update_fields=["view_count"])

        return ad


@extend_schema(
    tags=["Store"], description="Eng mashhur mahsulotlar ro'yxatini kamayish tartibida qaytarish"
)
@custom_response
class AdPopularListView(generics.ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = CategoryProductUnionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["view_count"]
    ordering = ["-view_count"]


@extend_schema(tags=["Store"], description="Kategoriya va mahsulotlarni qidiruv bo‘yicha qaytarish")
@custom_response
class CategoryProductSearchView(generics.ListAPIView):
    serializer_class = CategoryProductUnionSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        query = self.request.query_params.get("q")
        categories = (
            Category.objects.filter(name__icontains=query) if query else Category.objects.none()
        )
        products = Ad.objects.filter(name__icontains=query) if query else Ad.objects.none()

        return list(categories) + list(products)
