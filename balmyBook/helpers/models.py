from django.db import models


# A class to help create created_at and modified_at
class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        # latest record first
        ordering = ("-created_at",)
