from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import forms
from . import models
from events.models import Event


# Create Post

class CreatePost(LoginRequiredMixin, generic.CreateView):

    form_class = forms.PostForm
    model = models.Post

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        slug = self.object.event.slug
        return reverse("events:single", kwargs={"slug": slug})

# Delete Post

class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):

        model = models.Post
        select_related = ("user", "event")

        def get_queryset(self):

            queryset = super().get_queryset()
            return queryset.filter(user_id=self.request.user.id)

        def delete(self, *args, **kwargs):

            messages.success(self.request, "Message successfully deleted")
            return super().delete(*args, **kwargs)

        def get_success_url(self):
            slug = self.object.event.slug
            return reverse("events:single", kwargs={"slug": slug})

# Timeline of user posts (currently not being used)

class UserPosts(generic.ListView):

    model = models.Post
    template_name = "posts/user_timeline.html"

    def get_queryset(self):

        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:

            raise Http404
        else:

            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user

        return context

# Single Post View

class SinglePost(SelectRelatedMixin, generic.DetailView):

    model = models.Post
    select_related = ("user", "event")

    def get_queryset(self):

        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )