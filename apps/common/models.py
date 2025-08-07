import uuid

from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Page(BaseModel):
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, unique=True)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Region(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class District(BaseModel):
    region = models.ForeignKey(Region, related_name="districts", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        unique_together = ["region", "name"]

    def __str__(self):
        return self.name


class Setting(BaseModel):
    phone = models.CharField(max_length=20)
    support_email = models.EmailField()
    working_hours = models.CharField(max_length=100)
    app_version = models.CharField(max_length=50)
    maintenance_mode = models.BooleanField(default=False)

    def __str__(self):
        return "Settings"
