from django.urls import path

from . import views

urlpatterns = [
    path("category/", views.CategoryListView.as_view(), name="categories"),
    path(
        "categories-with-children/",
        views.CategoryWithChildrenView.as_view(),
        name="categories-with-children",
    ),
    path("sub-category/", views.SubCategoryListView.as_view(), name="sub-categories"),
    path(
        "product-download/<slug:slug>/",
        views.ProductDownloadView.as_view(),
        name="product-download",
    ),
    path("product-image-create/", views.AdImageCreateView.as_view(), name="product-image-create"),
    path("ads/", views.AdCreateView.as_view(), name="ad-create"),
    path("list/ads/", views.AdListView.as_view(), name="ads-list"),
    path("ads/<slug:slug>/", views.AdDetailView.as_view(), name="ad-detail"),
    path(
        "favourite-product-create/",
        views.FavouriteProductCreateView.as_view(),
        name="favourite-create",
    ),
    path(
        "favourite-product-create-by-id/",
        views.FavouriteProductCreateByIDView.as_view(),
        name="favourite-create-by-id",
    ),
    path(
        "favourite-product/<int:product_id>/delete/",
        views.FavouriteProductDeleteView.as_view(),
        name="favourite-delete",
    ),
    path(
        "favourite-product-by-id/<int:product_id>/delete/",
        views.FavouriteProductDeleteByDeviceView.as_view(),
        name="favourite-delete-by-id",
    ),
    path(
        "my-favourite-product/",
        views.MyFavouriteProductListView.as_view(),
        name="favourite-product",
    ),
    path(
        "my-favourite-product-by-id/",
        views.MyFavouriteProductByIDListView.as_view(),
        name="favourite-product-by-id",
    ),
    path("my-ads/", views.MyAdListView.as_view(), name="my-ads-list"),
    path("my-ads/<int:pk>/", views.MyAdDetailView.as_view(), name="my-ad-detail"),
    path("my-search/", views.MySearchCreateView.as_view(), name="my-search-create"),
    path("my-search/list/", views.MySearchListView.as_view(), name="my-search-list"),
    path("my-search/<int:id>/delete/", views.MySearchDeleteView.as_view(), name="my-search-delete"),
    path(
        "search/category-product/",
        views.CategoryProductSearchView.as_view(),
        name="categories-products",
    ),
    path("search/complete/", views.AdSearchView.as_view(), name="search-complete"),
    path(
        "search/count-increase/<int:id>/",
        views.CountIncreaseView.as_view(),
        name="search-count-increase",
    ),
    path("search/populars/", views.AdPopularListView.as_view(), name="populars"),
]
