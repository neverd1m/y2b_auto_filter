# Generated by Django 3.2.2 on 2021-05-17 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_filters', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='filter',
            name='category',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='filter',
            name='videos',
            field=models.ManyToManyField(blank=True, null=True, related_name='filters', to='blog_app.Video'),
        ),
    ]