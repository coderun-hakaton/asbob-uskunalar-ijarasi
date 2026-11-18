from django.db import migrations, models
import django.db.models.deletion
from django.db.models import Q
import django.core.validators


TOOLS = [
    {
        "code": "A01",
        "name": "Drel",
        "description": "Ta'mirlash va montaj ishlari uchun qulay elektr drel.",
        "daily_rate": 30000,
        "category": "construction",
        "icon": "🔩",
    },
    {
        "code": "A02",
        "name": "Narvon",
        "description": "Uy ichidagi balandlikda bajariladigan ishlar uchun.",
        "daily_rate": 20000,
        "category": "home",
        "icon": "🪜",
    },
    {
        "code": "A03",
        "name": "Proyektor",
        "description": "Taqdimotlar va kino kechalari uchun tiniq tasvir.",
        "daily_rate": 100000,
        "category": "event",
        "icon": "📽️",
    },
    {
        "code": "A04",
        "name": "Mikrofon",
        "description": "Kichik tadbir va chiqishlar uchun sifatli ovoz.",
        "daily_rate": 40000,
        "category": "event",
        "icon": "🎙️",
    },
    {
        "code": "A05",
        "name": "Tikuv mashinasi",
        "description": "Uy sharoitidagi tikuv va ta'mirlash ishlari uchun.",
        "daily_rate": 60000,
        "category": "craft",
        "icon": "🧵",
    },
    {
        "code": "A06",
        "name": "Gilam tozalagich",
        "description": "Gilam va yumshoq mebellarni chuqur tozalash uchun.",
        "daily_rate": 80000,
        "category": "home",
        "icon": "🧹",
    },
]


def add_initial_tools(apps, schema_editor):
    Tool = apps.get_model("rentals", "Tool")
    Tool.objects.using(schema_editor.connection.alias).bulk_create(
        [Tool(**tool) for tool in TOOLS]
    )


def remove_initial_tools(apps, schema_editor):
    Tool = apps.get_model("rentals", "Tool")
    Tool.objects.using(schema_editor.connection.alias).filter(
        code__in=[tool["code"] for tool in TOOLS]
    ).delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tool",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=10, unique=True, verbose_name="Kodi")),
                ("name", models.CharField(max_length=100, verbose_name="Nomi")),
                ("description", models.CharField(max_length=240, verbose_name="Tavsif")),
                ("daily_rate", models.PositiveIntegerField(verbose_name="Kunlik narx")),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("construction", "Qurilish"),
                            ("home", "Uy uchun"),
                            ("event", "Tadbir"),
                            ("craft", "Hunarmandchilik"),
                        ],
                        max_length=20,
                        verbose_name="Toifa",
                    ),
                ),
                ("icon", models.CharField(max_length=10, verbose_name="Belgi")),
                ("is_available", models.BooleanField(default=True, verbose_name="Ijaraga beriladi")),
            ],
            options={
                "verbose_name": "Asbob",
                "verbose_name_plural": "Asboblar",
                "ordering": ["code"],
            },
        ),
        migrations.CreateModel(
            name="Rental",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_name", models.CharField(max_length=100, verbose_name="Mijoz ismi")),
                (
                    "days",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(7),
                        ],
                        verbose_name="Kunlar soni",
                    ),
                ),
                ("daily_rate", models.PositiveIntegerField(verbose_name="Ijara vaqtidagi kunlik narx")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")),
                (
                    "tool",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="rentals",
                        to="rentals.tool",
                        verbose_name="Asbob",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ijara so'rovi",
                "verbose_name_plural": "Ijara so'rovlari",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="rental",
            constraint=models.CheckConstraint(
                condition=Q(("days__gte", 1), ("days__lte", 7)),
                name="rental_days_between_1_and_7",
            ),
        ),
        migrations.RunPython(add_initial_tools, remove_initial_tools),
    ]
