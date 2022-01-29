import uuid
from pyexpat import model
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.

class Post(models.Model):
    text = models.TextField("content", max_length=300)
    date = models.DateTimeField("date", default=timezone.now)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date', ]

    def __str__(self) -> str:
        return self.text

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    partner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='partner') #partner側
    myname = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='myname') #自分側
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)