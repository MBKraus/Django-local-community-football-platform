
from .models import Event
from django import forms
from django.forms import Textarea

class CreateForm(forms.ModelForm):

    class Meta:

        model = Event
        fields = ['name', 'description', 'date', 'address', 'time']
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control',
                                           'id': 'DateField', 'min': '2017-01-01'}),
            'time': forms.TextInput(attrs={'type': 'time', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'cols': 80, 'rows': 10, 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UpdateForm(forms.ModelForm):

    class Meta:

        model = Event
        fields = ['name', 'description', 'date', 'address', 'time']
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control',
                                           'id': 'DateField', 'min': '2017-01-01'}),
            'time': forms.TextInput(attrs={'type': 'time', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'cols': 80, 'rows': 10, 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'onFocus': 'geolocate()', 'name': 'address',}),
        }
