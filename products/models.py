from django.db import models
import uuid


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField()
    category = models.CharField(max_length=50)
    user = models.ForeignKey(
        "users.User",
        related_name="products",
        on_delete=models.CASCADE,
    )
    carts = models.ManyToManyField("carts.Cart", through="products.ProductCart",related_name="products")

class ProductCart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    product = models.ForeignKey(
        "products.Product",
        related_name= "carts_product",
        on_delete= models.CASCADE
    )
    cart = models.ForeignKey(
        "carts.Cart",
        related_name= "products_cart",
        on_delete= models.CASCADE
    )
    quantity = models.PositiveIntegerField()



