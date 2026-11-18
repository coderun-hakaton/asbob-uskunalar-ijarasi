from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RentalForm
from .models import Tool


def catalog(request):
    tools = Tool.objects.filter(is_available=True)
    return render(request, "rentals/index.html", {"tools": tools})


def create_rental(request, tool_id):
    tool = get_object_or_404(Tool, pk=tool_id, is_available=True)
    if request.method != "POST":
        return redirect("catalog")

    form = RentalForm(request.POST)
    if form.is_valid():
        rental = form.save(commit=False)
        rental.tool = tool
        rental.daily_rate = tool.daily_rate
        rental.save()
        messages.success(
            request,
            (
                f"So'rov qabul qilindi: {tool.name}, {rental.days} kun — "
                f"{rental.total_price:,} so'm."
            ).replace(",", " "),
        )
        return redirect("catalog")

    return render(
        request,
        "rentals/index.html",
        {
            "tools": Tool.objects.filter(is_available=True),
            "rental_tool": tool,
            "rental_form": form,
        },
        status=400,
    )
