from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/<str:username>/', views.user_profile, name='profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path("", views.TopView.as_view(), name="top"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]