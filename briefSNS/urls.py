from django.urls import path
from . import views

app_name = 'briefSNS'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post_list', views.PostListView.as_view(), name='post_list'),
    path('post_create', views.PostCreateView.as_view(), name='post_create'),
    path('post_detail/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post_update/<int:pk>', views.PostUpdatelView.as_view(), name='post_update'),
    path('post_delete/<int:pk>', views.PostDeleteView.as_view(), name='post_delete'),
    path('playgroung', views.PlaygroundView.as_view(), name='playground'),
    path('dm/<str:partnername>/<str:username>/', views.DMview.as_view(), name='dm'),
]