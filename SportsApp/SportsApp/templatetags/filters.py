from django import template

register = template.Library()

@register.filter(name='percentformat')
def percentformat(value):
    return round(float(value) * 100,1)