import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Borrowing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey("book.Book", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        ordering = ["-borrow_date"]
        verbose_name_plural = _("Borrowing")
        verbose_name = _("Borrowing")

    def clean(self):
        borrow_date = self.borrow_date or now().date()
        if self.expected_return_date <= borrow_date:
            raise ValidationError(
                _("Expected return date must be after borrowing date.")
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.borrow_date} - {self.expected_return_date}"
