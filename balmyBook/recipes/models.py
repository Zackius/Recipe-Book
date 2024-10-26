from datetime import timezone
from django.db import models
import uuid

from balmyBook.helpers.models import TrackingModel
from balmyBook.user.models import User

# Create your models here.

class Recipe(TrackingModel):
    "A class to create a recipe"

    id= models.AutoField(primary_key=True)
    uuid = models.UUIDField(
        unique=True,
        editable=False, 
        default=uuid.uuid4,
        verbose_name="Public Identifier"
    )
    name = models.CharField(max_length=50, blank=False)
    ingredients = models.CharField(max_length=300, blank=False)
    procedure = models.CharField(max_length=500, blank=False)
    people_served = models.CharField(max_length=15, blank=False)
    cooking_time = models.CharField(max_length=15, blank=False)
    country_origin = models.CharField(max_length=20, blank=True)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_link = models.CharField(max_length=50, blank=True)
    image_url = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    


