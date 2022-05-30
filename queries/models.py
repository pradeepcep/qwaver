from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Database(models.Model):
    title = models.CharField(max_length=256, default="")
    host = models.CharField(max_length=256)
    port = models.IntegerField()
    database = models.CharField(max_length=256, default="")
    user = models.CharField(max_length=256)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class Query(models.Model):
    title = models.CharField(max_length=100)
    database = models.ForeignKey(Database, on_delete=models.CASCADE, default=0)
    query = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('query-detail', kwargs={'pk': self.pk})


class Parameter(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default="")
    default = models.CharField(max_length=256, blank=True, null=True)
    # if the user inputs a value for this field, then the template plus the value is inserted
    # e.g.: template_defined = "AND campaign_id = {v}"
    # whe the user inputs "54321", what is inserted in the query is "AND campaign_id = 54321"
    template = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('query-detail', kwargs={'pk': self.query.pk})


class Instance(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    # title based on specific input: e.g. input is 5, and title is "revenue past 5 days"
    # title = models.CharField(max_length=256)


class Result(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dataframe = models.JSONField()
    chart = models.TextField(default="")
    preview = models.TextField(default="")


# the specific value for an input field
class Value(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.CharField(max_length=256, default=""),
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)

