import uuid
from django.db import models
from django.utils.translation import get_language
from django.utils.text import slugify


class BaseModel(models.Model):
    guid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
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
            title_uz = getattr(self, 'title_uz', None)
            if title_uz:
                self.slug = slugify(title_uz)
            else:
                self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title