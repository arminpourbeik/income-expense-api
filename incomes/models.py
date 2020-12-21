from django.db import models

from authentication.models import User


class Income(models.Model):
    """
    Database table for incomes
    """

    INCOME_OPTIONS = (
        ("SALARY", "SALARY"),
        ("BUSINESS", "BUSINESS"),
        ("SIDE_HUSTLES", "SIDE_HUSTLES"),
        ("OTHERS", "OTHERS"),
    )

    source = models.CharField(choices=INCOME_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    date = models.DateField(null=False, blank=False)

    class Meta:
        ordering = ("-date",)

    def __str__(self) -> str:
        return f"{self.owner}'s income"