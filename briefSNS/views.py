from email import message
from django.views import generic
from .models import Post, Message
from .forms import PostCreateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
import os

class IndexView(generic.TemplateView):
    template_name = 'briefSNS/index.html'

class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post


class PostCreateView(LoginRequiredMixin,generic.CreateView):
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('briefSNS:post_list')
    def get_context_data(self):
        context = super().get_context_data()
        context['user'] = get_user_model().objects.get(username=self.request.user)
        print(context['user'].username.__str__())
        return context
    
    def form_valid(self, form):
       #qryset =  form.save(commit=False)
       #form.instance.user = self.request.user
       #ここのauthorはモデル定義時のauthorと紐づく
       form.instance.author = self.request.user
       #qryset.save()
       return super().form_valid(form)

class PostDetailView(generic.DetailView):
    model = Post

class PostUpdatelView(generic.UpdateView):
    model = Post
    form_class = PostCreateForm
    ccess_url = reverse_lazy("briefSNS:post_detail")

class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy("briefSNS:post_list")

class PlaygroundView(generic.TemplateView):
    template_name = "blog/playground.html"

class DMview(LoginRequiredMixin, generic.TemplateView):
    template_name = "briefSNS/dm.html"

    def get_context_data(self, partnername, username):
        context = super().get_context_data()
        partner = get_user_model().objects.get(username=partnername)
        user = get_user_model().objects.get(username=username)
        context['partner'] = partner
        context['user'] = user
        messages1 = Message.objects.filter(partner=partner.pk, myname=user.pk)
        messages2 = Message.objects.filter(partner=user.pk, myname=partner.pk)
        messages = messages1.union(messages2).order_by("-created_at")

        context['forDebug'] = str(type(partner.pk))
        context['messages'] = messages
        context['partnerpk'] = partner.pk
        context['userpk'] = user.pk
        port = os.environ["PORT"]
        context['for_script'] =  {"partnername":partnername, "username":username, "partnerpk":partner.pk, "userpk":user.pk, "port":port}
        return context
    
    def form_valid(self, form):
       #qryset =  form.save(commit=False)
       #form.instance.user = self.request.user
       #ここのauthorはモデル定義時のauthorと紐づく
       form.instance.myname = self.request.user
       #qryset.save()
       return super().form_valid(form)