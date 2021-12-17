from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def minutes(time):
    if isinstance(time, timedelta):
        return time.seconds // 60
    return time