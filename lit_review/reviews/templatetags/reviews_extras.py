from django import template
from django.utils import timezone

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.filter
def time_created_display(time_created):
    seconds_ago = (timezone.now() - time_created).total_seconds()
    if seconds_ago <= HOUR:
        return f'il y a {int(seconds_ago // MINUTE)} minutes.'
    elif seconds_ago <= DAY:
        return f'il y a {int(seconds_ago // HOUR)} heures.'
    return f'le {time_created.strftime("%d %b %y à %Hh%M")}'


@register.simple_tag(takes_context=True)
def get_user_display(context, user):
    return 'vous' if user == context['user'] else user.username
