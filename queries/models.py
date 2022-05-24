from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Query(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('query-detail', kwargs={'pk': self.pk})
