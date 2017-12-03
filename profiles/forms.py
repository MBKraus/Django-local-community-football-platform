from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
#from django.forms.extras.widgets import SelectDateWidget
from django.forms import SelectDateWidget
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Invalid Username or Password",
        'inactive': "This is not an active profile",
    }

    def __init__(self, *args, **kwargs):
            super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
            self.fields['username'].label = 'Username'
            self.fields['password'].label = 'Password'


class UserCreateForm(UserCreationForm):

    error_messages = {
        'password_mismatch': "The two passwords you entered do not match.",
    }
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                help_text="Enter the chosen password once more")

    class Meta:

        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["email"].label = "E-mail address"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Repeat password"

class UserProfileForm(forms.ModelForm):

    class Meta:

        model = User
        fields = ('email', 'bio', 'date_of_birth')
        widgets = {
            'date_of_birth': SelectDateWidget(years=range(1950, 2017)),
        }

    def save(self, user=None):

        user_profile = super(UserProfileForm, self).save(commit=False)

        if user:

            user_profile.user = user
            user_profile.save()

        return user_profile

class ProfileForm(forms.ModelForm):

    class Meta:

         model = User
         fields = ('username', 'email', 'bio', 'date_of_birth', 'position')
         widgets = {
                    'email': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
                    'bio': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
                    'date_of_birth': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
                }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["email"].label = "E-mail address"
        self.fields["date_of_birth"].label = "Date of birth"
        self.fields["position"].label = "Favorite position"
