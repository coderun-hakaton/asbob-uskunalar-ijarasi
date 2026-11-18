from django import forms

from .models import Rental


class RentalForm(forms.ModelForm):
    customer_name = forms.CharField(
        label="Mijoz ismi",
        max_length=100,
        strip=True,
        error_messages={"required": "Ism maydoni bo'sh qolishi mumkin emas."},
        widget=forms.TextInput(
            attrs={
                "placeholder": "Masalan, Jasur",
                "autocomplete": "name",
                "maxlength": 100,
            }
        ),
    )
    days = forms.IntegerField(
        label="Kunlar soni",
        min_value=1,
        max_value=7,
        error_messages={
            "required": "Kunlar sonini kiriting.",
            "invalid": "Kunlar soni butun son bo'lishi kerak.",
            "min_value": "Ijara muddati kamida 1 kun bo'lishi kerak.",
            "max_value": "Kunlar soni 1 dan 7 gacha bo'lishi kerak.",
        },
        widget=forms.NumberInput(
            attrs={"min": 1, "max": 7, "step": 1, "value": 1}
        ),
    )

    class Meta:
        model = Rental
        fields = ["customer_name", "days"]

    def clean_customer_name(self):
        name = self.cleaned_data["customer_name"].strip()
        if not name:
            raise forms.ValidationError("Ism maydoni bo'sh qolishi mumkin emas.")
        return name
