from django.contrib import admin

from .models import Event, EventMember

class EventMemberInline(admin.TabularInline):
    model = EventMember

class EventAdmin(admin.ModelAdmin):
    inlines = [EventMemberInline]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'date', 'address']
    list_filter = ['name', 'date', 'address']
    list_display = ['name', 'date', 'address']
    list_editable = ['date']

admin.site.register(Event, EventAdmin)