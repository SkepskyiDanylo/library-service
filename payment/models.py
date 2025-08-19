import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PAID = "PAID", _("Paid")

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT", _("Payment")
        FINE = "FINE", _("Fine")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    borrowing = models.ForeignKey(
        "borrowing.Borrowing",
        on_delete=models.PROTECT,
        related_name="payments",
    )
    session_url = models.URLField()
    session_id = models.CharField(
        max_length=255,
        unique=True,
    )
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.PAYMENT)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return f"{self.money_to_pay}$ - {self.borrowing}"
