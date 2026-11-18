from django.test import TestCase
from django.urls import reverse

from .models import Rental, Tool


class RentalFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tool = Tool.objects.get(code="A01")

    def test_catalog_shows_seeded_tools_and_categories(self):
        response = self.client.get(reverse("catalog"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["tools"].count(), 6)
        self.assertContains(response, "Drel")
        self.assertContains(response, "Qurilish")
        for code in ("a01", "a02", "a03", "a04", "a05", "a06"):
            self.assertContains(
                response,
                f"/static/rentals/images/{code}.svg",
            )

    def test_valid_rental_is_saved_with_server_calculated_rate(self):
        response = self.client.post(
            reverse("create_rental", args=[self.tool.pk]),
            {"customer_name": "  Jasur  ", "days": "3"},
        )

        self.assertRedirects(
            response,
            reverse("catalog"),
            fetch_redirect_response=False,
        )
        rental = Rental.objects.get()
        self.assertEqual(rental.customer_name, "Jasur")
        self.assertEqual(rental.days, 3)
        self.assertEqual(rental.daily_rate, self.tool.daily_rate)
        self.assertEqual(rental.total_price, 90000)
        self.assertContains(self.client.get(reverse("catalog")), "qabul qilindi")

    def test_invalid_days_and_blank_name_do_not_create_rental(self):
        response = self.client.post(
            reverse("create_rental", args=[self.tool.pk]),
            {"customer_name": "   ", "days": "8"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Rental.objects.count(), 0)
        self.assertContains(response, "1 dan 7 gacha", status_code=400)
        self.assertContains(response, "Ism maydoni", status_code=400)

    def test_unavailable_tool_cannot_be_rented(self):
        self.tool.is_available = False
        self.tool.save(update_fields=["is_available"])

        response = self.client.post(
            reverse("create_rental", args=[self.tool.pk]),
            {"customer_name": "Jasur", "days": "1"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Rental.objects.count(), 0)
