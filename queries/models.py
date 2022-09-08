from django.db import models
from django.db.models import ManyToManyField
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from users.models import Organization


# Database connection information
class Database(models.Model):
    MYSQL = 'MySQL'
    POSTGRES = 'PostgreSQL'
    REDSHIFT = 'Redshift'
    MARIADB = 'MariaDB'
    ORACLE = 'Oracle'
    CHOICES = (
        (MYSQL, MYSQL),
        (POSTGRES, POSTGRES),
        (REDSHIFT, REDSHIFT),
        (MARIADB, MARIADB),
        (ORACLE, ORACLE),
        (REDSHIFT, REDSHIFT)
    )
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, default=1)
    title = models.CharField(max_length=256, default="", help_text='Can be any name you want such as "Transaction events"')
    host = models.CharField(max_length=256)
    port = models.IntegerField()
    database = models.CharField(max_length=256, default="", help_text="The name of the database on your server")
    user = models.CharField(max_length=256, help_text="Ideally with read-only permissions")
    password = models.CharField(max_length=256)
    platform = models.CharField(
        max_length=64,
        choices=CHOICES, default=MYSQL
    )
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Query(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=256, null=True, blank=True)
    database = models.ForeignKey(Database, on_delete=models.CASCADE, null=False, blank=False)
    query = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    run_count = models.IntegerField(default=0)
    last_run_date = models.DateTimeField(default=None, null=True)
    # https://stackoverflow.com/questions/34003865/django-reverse-query-name-clash
    latest_result = models.ForeignKey("queries.Result", related_name='+', on_delete=models.DO_NOTHING, null=True)
    # Set when a query is first run
    is_valid = models.BooleanField(default=False)
    # A running count for how many consecutive errors have happened recently.
    # Reset to 0 if the query is successfully executed
    recent_error_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('query-detail', kwargs={'pk': self.pk})

    def get_params(self):
        return Parameter.objects.filter(query=self)


class Parameter(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, default="")
    default = models.CharField(max_length=256, blank=True, null=True)
    # if the user inputs a value for this field, then the template plus the value is inserted
    # e.g.: template_defined = "AND campaign_id = {v}"
    # whe the user inputs "54321", what is inserted in the query is "AND campaign_id = 54321"
    template = models.CharField(max_length=256, blank=True, null=True, help_text='for example: "AND timestamp > {v}"')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('query-detail', kwargs={'pk': self.query.pk})

    @property
    def form_name(self):
        return self.name.replace(" ", "_")


class Result(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True)
    dataframe = models.TextField(null=True)
    table = models.TextField(null=True)
    single = models.CharField(max_length=64, null=True)
    image_encoding = models.CharField(max_length=16, null=True)
    chart = models.TextField(null=True)
    preview = models.TextField(null=True)


# the specific value for an input field
class Value(models.Model):
    parameter_name = models.CharField(max_length=64, default="")
    value = models.CharField(max_length=256, default="")
    result = models.ForeignKey(Result, on_delete=models.CASCADE)


class UserSearch(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    search = models.CharField(max_length=64, default="")


class QueryComment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    comment = models.TextField(null=True)