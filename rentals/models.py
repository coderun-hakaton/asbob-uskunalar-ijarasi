from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Tool(models.Model):
    class Category(models.TextChoices):
        CONSTRUCTION = "construction", "Qurilish"
        HOME = "home", "Uy uchun"
        EVENT = "event", "Tadbir"
        CRAFT = "craft", "Hunarmandchilik"

    code = models.CharField("Kodi", max_length=10, unique=True)
    name = models.CharField("Nomi", max_length=100)
    description = models.CharField("Tavsif", max_length=240)
    daily_rate = models.PositiveIntegerField("Kunlik narx")
    category = models.CharField(
        "Toifa",
        max_length=20,
        choices=Category.choices,
    )
    icon = models.CharField("Belgi", max_length=10)
    is_available = models.BooleanField("Ijaraga beriladi", default=True)

    class Meta:
        ordering = ["code"]
        verbose_name = "Asbob"
        verbose_name_plural = "Asboblar"

    def __str__(self):
        return f"{self.name} ({self.code})"


class Rental(models.Model):
    tool = models.ForeignKey(
        Tool,
        on_delete=models.PROTECT,
        related_name="rentals",
        verbose_name="Asbob",
    )
    customer_name = models.CharField("Mijoz ismi", max_length=100)
    days = models.PositiveSmallIntegerField(
        "Kunlar soni",
        validators=[MinValueValidator(1), MaxValueValidator(7)],
    )
    daily_rate = models.PositiveIntegerField("Ijara vaqtidagi kunlik narx")
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Ijara so'rovi"
        verbose_name_plural = "Ijara so'rovlari"
        constraints = [
            models.CheckConstraint(
                condition=Q(days__gte=1) & Q(days__lte=7),
                name="rental_days_between_1_and_7",
            ),
        ]

    def __str__(self):
        return f"{self.tool.name} — {self.customer_name}"

    @property
    def total_price(self):
        return self.daily_rate * self.days
