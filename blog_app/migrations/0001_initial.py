# Generated by Django 3.2.2 on 2021-05-15 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя видео')),
                ('youtube_id', models.CharField(max_length=100, verbose_name='Идентификатор видео')),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('category', models.CharField(max_length=200)),
                ('subscriber', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='videos')),
            ],
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text_request', models.CharField(max_length=200)),
                ('published_after', models.DateTimeField(blank=True, null=True)),
                ('category', models.CharField(max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_filters', to=settings.AUTH_USER_MODEL)),
                ('subscribers', models.ManyToManyField(related_name='sub_filters', to=settings.AUTH_USER_MODEL)),
                ('videos', models.ManyToManyField(related_name='filters', to='blog_app.Video')),
            ],
        ),
    ]
