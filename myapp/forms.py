from django import forms
from django.forms import HiddenInput
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from .models import Client, AdventureType, Adventure, CreateEvent, EventBooking


class ClientForm(forms.ModelForm):
    confirmpassword = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Client
        fields = ['username', 'email', 'password', 'confirmpassword', 'first_name', 'last_name', 'IsAdmin']
        widgets = {
            'password': forms.PasswordInput()
        }


class CreateEventForm(forms.ModelForm):
    class Meta:
        model = CreateEvent
        fields = ['name', 'description', 'advanture', 'location', 'price', 'event_date', 'img']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form__input'}),
            'img': forms.FileInput(attrs={'class': 'form__input'}),
            'name': forms.TextInput(attrs={'class': 'form__input'}),
            'location': forms.TextInput(attrs={'class': 'form__input'}),
            'description': forms.Textarea(attrs={'class': 'form__input', }),
            'advanture': forms.Select(attrs={'class': 'form__input', }),
            'price': forms.NumberInput(attrs={'class': 'form__input', })
            # 'price': forms.TextInput(attrs={'class': 'form__input'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)
        self.fields['advanture'].queryset = Adventure.objects.all()


class EventBookingForm(forms.ModelForm):
    class Meta:
        model = EventBooking
        fields = ['number_of_people']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number_of_people'].widget.attrs.update({'class': 'form-control'})
