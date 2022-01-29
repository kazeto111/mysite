from django.contrib.auth import get_user_model
from django.shortcuts import render
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.views import generic
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

def user_profile(request, username):
    user_object = get_user_model().objects.get(username=username)
    context = {
        'User': user_object,
        "Post_list": user_object.posts.all()
    }
    print(dir(context["User"]))
    print(context["User"].posts.all())

    return render(request, 'accounts/user_profile.html', context)

class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy('briefSNS:post_list')

class TopView(generic.TemplateView):
    template_name = "accounts/top.html"

class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = "accounts/home.html"

class LoginView(LoginView):
    """ログインページ"""
    form_class = forms.LoginForm
    template_name = "accounts/login.html"

class LogoutView(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = "accounts/logout.html"