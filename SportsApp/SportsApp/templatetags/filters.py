from django import template

register = template.Library()

@register.filter(name='percentformat')
def percentformat(value):
    return round(float(value) * 100,1)

@register.filter(name='addstrings')
def addstrings(s1, s2):
    s1 = str(s1)
    s2 = str(s2)
    if ' ' in str(s1):
        s1 = s1.replace(' ', '_')
    if ' ' in str(s2):
        s2 = s2.replace(' ', '_')
    return s1 + s2

@register.filter(name='calcpercent')
def calcpercent(n, d):
    return round(float(n/d) * 100, 1)