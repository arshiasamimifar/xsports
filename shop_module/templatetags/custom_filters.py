from django import template

register = template.Library()


@register.filter
def intcomma(value):
    if value is None:
        return ''
    return f"{value:,}"
