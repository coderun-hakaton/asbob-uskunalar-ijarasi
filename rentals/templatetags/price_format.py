from django import template


register = template.Library()


@register.filter
def space_grouped(value):
    return f"{int(value):,}".replace(",", " ")
