from common.models import BaseModel
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon = models.ImageField(upload_to="category_icons/", null=True, blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ad(BaseModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        ARCHIVED = "archived", "Archived"

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    seller = models.ForeignKey(
        "accounts.CustomUser", related_name="products", on_delete=models.CASCADE
    )
    address = models.ForeignKey("accounts.Address", on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AdImage(BaseModel):
    ad = models.ForeignKey(Ad, related_name="photos", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="ads/")
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ad.name} - {self.image.name}"


class FavouriteProduct(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favourites",
        null=True,
        blank=True,
    )
    product = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="favourited_by")
    device_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ("user", "product", "device_id")

    def __str__(self):
        return f"{self.user or self.device_id} - {self.product}"


class SearchHistoryQuerySet(models.QuerySet):
    def for_request(self, request):
        user = request.user if request.user.is_authenticated else None
        device_id = request.query_params.get("device_id")
        if user:
            return self.filter(user=user)
        if device_id:
            return self.filter(device_id=device_id)
        return self.none()


class SearchHistory(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="search_histories",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    device_id = models.CharField(max_length=255, blank=True, null=True)
    query = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=1)
    objects = SearchHistoryQuerySet.as_manager()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="my_searches", null=True, blank=True
    )
    price_min = models.PositiveIntegerField(null=True, blank=True)
    price_max = models.PositiveIntegerField(null=True, blank=True)
    region_id = models.ForeignKey(
        "common.Region",
        on_delete=models.SET_NULL,
        related_name="my_searches",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return f"{self.query} ({self.count})"


class SearchCount(models.Model):
    product = models.OneToOneField(
        "store.Ad", on_delete=models.CASCADE, related_name="search_count_obj"
    )
    search_count = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} ({self.search_count})"
