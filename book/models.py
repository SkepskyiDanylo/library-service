from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):

    class Cover(models.TextChoices):
        HARD = "HARD", _("Hardcover")
        SOFT = "SOFT", _("Softcover")

    name = models.CharField(max_length=255, help_text=_("Book name"))
    pub_date = models.DateTimeField(help_text=_("Publication date"))
    author = models.CharField(max_length=255, help_text=_("Author full name"))
    cover = models.CharField(
        max_length=4,
        choices=Cover.choices,
        default=Cover.HARD,
        help_text=_("Cover type"),
    )
    inventory = models.PositiveIntegerField(default=1, help_text=_("Inventory"))
    daily_fee = models.DecimalField(
        max_digits=5, decimal_places=2, help_text=_("Daily fee in usd $")
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return f"{self.author}{self.pub_date} - {self.name}"
