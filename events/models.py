from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.text import slugify

from datetime import datetime



MEMBERSHIP_CHOICES = (
    (0, "banned"),
    (1, "member"),
    (2, "moderator"),
    (3, "admin")
)

class Event(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(max_length=500)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="EventMember")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+', null=True, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=18, decimal_places=13, null=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=13, null=True)
    time = models.TimeField(null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("events:single", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "events"


class EventMember(models.Model):

    event = models.ForeignKey(Event, related_name="memberships", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="events", on_delete=models.CASCADE)

    def __str__(self):
        return "{} is in {}".format(
            self.user.username,
            self.event.name
        )

    class Meta:
        unique_together = ("event", "user")

