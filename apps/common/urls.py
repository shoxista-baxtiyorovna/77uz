from django.urls import path

from .views import PageDetailView, PageListView, RegionWithDistrictsView, SettingRetrieveView

urlpatterns = [
    path("pages/", PageListView.as_view(), name="pages"),
    path("pages/<slug:slug>/", PageDetailView.as_view(), name="page-by-slug"),
    path("regions-with-districts/", RegionWithDistrictsView.as_view(), name="region-districts"),
    path("setting/", SettingRetrieveView.as_view(), name="setting"),
]
