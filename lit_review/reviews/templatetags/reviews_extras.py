import locale
from django import template
from django.utils import timezone, safestring
from reviews import models

locale.setlocale(locale.LC_TIME, "fr_FR")

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
        return f'il y a {int(seconds_ago // MINUTE)} minutes'
    elif seconds_ago <= DAY:
        return f'il y a {int(seconds_ago // HOUR)} heures'
    return f'{time_created.strftime("%H:%M, %d %B %y")}'


@register.simple_tag()
def check_replied_ticket(ticket_id):
    reviews = models.Review.objects.all()
    replied_tickets = [review.ticket.id for review in reviews]
    if ticket_id not in replied_tickets:
        return safestring.mark_safe(
            '<a class="button" href="{% url \'create_reply_review\' ticket.id %}">Répondre</a>')
    else:
        return safestring.mark_safe('')


@register.simple_tag(takes_context=True)
def get_user_display(context, user):
    return 'vous' if user == context['user'] else user.username
