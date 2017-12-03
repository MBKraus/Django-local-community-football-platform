from django import template

from .. import models

register = template.Library()


@register.simple_tag
def get_all_events():

    return models.Event.objects.values_list("name")[:2]

@register.simple_tag(takes_context=True)
def get_user_events(context):

    return context["user"].events.select_related("event").all()

@register.simple_tag(takes_context=True)
def get_other_events(context):

    if context["user"].is_authenticated():

        return models.Event.objects.exclude(
            pk__in=context["user"].events.select_related(
                "event").values_list("event")
        )

    return models.Event.objects.all()

@register.inclusion_tag("events/_buttons_new.html", takes_context=True)
def event_buttons_new(context, event):

    user = context["user"]
    response = {"event": event, "in_event": False, "created_by_user": False,}

    if user in event.members.all():

        response["in_event"] = True

    if user == event.created_by:
            response["created_by_user"] = True

    return response

