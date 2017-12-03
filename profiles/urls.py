from django.conf.urls import url

from . import views

app_name = 'profiles'

urlpatterns = [
    url(
        r"login/$",
        views.LoginView.as_view(),
        name="login")
    ,
    url(
        r"logout/$",
        views.LogoutView.as_view(),
        name="logout"
    ),
    url(
        r"signup/$",
        views.SignUp.as_view(),
        name="signup"
    ),
    url(
        r"profile/$",
        views.get_profile,
        name="profile"
    ),
    url(
        r"profile/edit/$",
        views.ProfileEditView.as_view()
        , name='ProfileEdit'
    ),
    url(
        r"profile/(?P<username>\w+)/$",
        views.ProfileDetail,
        name='viewprofile'
    ),
    url(
        r"profile/password/reset/$",
        views.PW_ResetView.as_view(),
        name='PasswordReset'

    ),

    ]


