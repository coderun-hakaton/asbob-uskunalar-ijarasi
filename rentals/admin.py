from django.contrib import admin

from .models import Rental, Tool


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "category", "daily_rate", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("code", "name", "description")
    list_editable = ("daily_rate", "is_available")


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("tool", "customer_name", "days", "daily_rate", "created_at")
    list_filter = ("created_at", "tool")
    search_fields = ("customer_name", "tool__name", "tool__code")
    readonly_fields = ("tool", "customer_name", "days", "daily_rate", "created_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
