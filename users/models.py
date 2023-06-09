from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    is_seller = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cart = models.ForeignKey(
        "carts.Cart",
        related_name="user",
        on_delete=models.SET_NULL,
        null=True,
    )
    address = models.ForeignKey(
        "addresses.Address", related_name="user", on_delete=models.CASCADE
    )



