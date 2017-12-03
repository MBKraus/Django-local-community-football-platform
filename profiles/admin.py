from django.contrib import admin

from .models import User
from events.models import EventMember, Event

class EventMemberInline(admin.TabularInline):
    model = EventMember

class UserAdmin(admin.ModelAdmin):
    inlines = [EventMemberInline]
    search_fields = ['username', 'email', 'date_joined']
    list_display = ['username', 'email', 'date_joined']

admin.site.register(User, UserAdmin)
