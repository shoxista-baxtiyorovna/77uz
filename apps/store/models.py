from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon = models.URLField(max_length=500, blank=True, null=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
