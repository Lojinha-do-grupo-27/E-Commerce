from django.db import models
import uuid

class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True)
    price = models.FloatField()
    is_available = models.BooleanField()
    category = models.CharField(max_length=50)
    
    user = models.ForeignKey(
        "users.User",
        related_name="orders",
        on_delete=models.CASCADE
    )
    