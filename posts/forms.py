from django import forms

from . import models
from events.models import Event

class PostForm(forms.ModelForm):

    class Meta:

        fields = ("message", "event")
        model = models.Post
        labels = {
            'message': 'Bericht', 'event': 'Selecteer wedstrijd',
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user is not None:

            self.fields["event"].queryset = (
                Event.objects.filter(members__email__icontains=user.email)
            )
