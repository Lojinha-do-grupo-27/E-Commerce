from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField


class StatusChoices(models.TextChoices):
    PEDIDO_REALIZADO = "realizado"
    EM_ANDAMENTO = "andamento"
    ENTREGUE = "entregue"


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    products_ids = (ArrayField(models.CharField(max_length=50)),)
    status = models.CharField(
        max_length=30,
        choices=StatusChoices.choices,
        default=StatusChoices.PEDIDO_REALIZADO,
    )
    seller_id = models.CharField(max_length=50)
    user = models.ForeignKey(
        "users.User", related_name="orders", on_delete=models.CASCADE
    )
