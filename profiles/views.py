from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, FormView, RedirectView, CreateView, DetailView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import get_template
import datetime

from . import models
from . import forms
from .forms import ProfileForm
from .forms import CustomAuthenticationForm
from django.contrib.auth.views import PasswordResetView

from events.models import EventMember, Event


# Personal Profile View

@login_required
def get_profile(request):

    startdate = datetime.date.today()
    enddatefuture = startdate + datetime.timedelta(weeks=50)
    enddatepast = startdate - datetime.timedelta(weeks=50)
    profile = get_object_or_404(models.User, username__iexact=request.user.username)
    events = EventMember.objects.filter(user__username__iexact=request.user.username)
    eventscomingup = Event.objects.filter(date__range=[startdate, enddatefuture], members__username__icontains=request.user.username).order_by('date')
    eventspast = Event.objects.filter(date__range=[enddatepast, startdate], members__username__icontains=request.user.username).order_by('date')

    return render(request, 'profiles/user_profile.html', {'profile': profile, 'events': events, 'eventscomingup': eventscomingup, 'eventspast': eventspast})

# Public Profile View

@login_required
def ProfileDetail(request, username):

    profile = get_object_or_404(models.User, username=username)

    return render(request, 'profiles/user_detail1.html', {'profile': profile})

# Profile Edit View

class ProfileEditView(LoginRequiredMixin, UpdateView):

    model = models.User
    form_class = ProfileForm
    template_name = "profiles/edit_profile.html"
    success_url = reverse_lazy('profiles:profile')

    def get_object(self):

        user = models.User.objects.get(username=self.request.user.username)
        return user

# Login

class LoginView(FormView):

    form_class = CustomAuthenticationForm
    success_url = reverse_lazy("home")
    template_name = "registration/login.html"

    def get_form(self, form_class=None):

        if form_class is None:

            form_class = self.get_form_class()

        return form_class(self.request, **self.get_form_kwargs())

    def form_valid(self, form):

        login(self.request, form.get_user())

        return super().form_valid(form)

# Logout

class LogoutView(RedirectView):

    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):

        logout(request)
        return super().get(request, *args, **kwargs)

# Sign up

class SignUp(CreateView):

    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):

        form.save()
        username = form.cleaned_data['username']
        recipient = [form.cleaned_data['email']]
        email_subject = 'FootballPlatform.nl - Confirmation Profile Activation'
        message = get_template('registration/email_signup.html').render(
                    {
                        'username': username,
                    }
                    )

        send_mail(email_subject,
                  message,
                 'info@FootballPlatform.nl',
                  recipient,
                  fail_silently=False,
                  html_message=message,
                  )

        return super(SignUp, self).form_valid(form)

# Password Reset View

class PW_ResetView(PasswordResetView):
   html_email_template_name = 'registration/password_reset_email.html'
