from django.urls import path

from . import views


urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("ijara/<int:tool_id>/", views.create_rental, name="create_rental"),
]
