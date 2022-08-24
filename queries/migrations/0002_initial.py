# Generated by Django 4.0.4 on 2022-08-24 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('queries', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='usersearch',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.organization'),
        ),
        migrations.AddField(
            model_name='usersearch',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='result',
            name='query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='queries.query'),
        ),
        migrations.AddField(
            model_name='result',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='querycomment',
            name='query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='queries.query'),
        ),
        migrations.AddField(
            model_name='querycomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='query',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='query',
            name='database',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='queries.database'),
        ),
        migrations.AddField(
            model_name='query',
            name='latest_result',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='queries.result'),
        ),
        migrations.AddField(
            model_name='parameter',
            name='query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='queries.query'),
        ),
        migrations.AddField(
            model_name='parameter',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='database',
            name='organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='users.organization'),
        ),
    ]
