from django.views.generic import TemplateView
from events.models import EventMember, Event

class Home(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):

        context = super(Home, self).get_context_data(**kwargs)
        context["event"] = Event.objects.all()
        return context



