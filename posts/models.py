from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.db import models
from datetime import datetime

from events.models import Event


class Post(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    event = models.ForeignKey(Event, related_name="posts",
                                  null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):

        return self.message

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def get_absolute_url(self):

        return reverse_lazy("events:single", kwargs={"slug": self.event.slug})

    class Meta:

        ordering = ["-created_at"]
        unique_together = ["user", "message"]
