# Generated by Django 3.1.2 on 2020-11-17 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import task.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=200)),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=task.models.upload_image_to)),
                ('anger', models.FloatField(blank=True, null=True, verbose_name='화남')),
                ('contempt', models.FloatField(blank=True, null=True, verbose_name='경멸')),
                ('disgust', models.FloatField(blank=True, null=True, verbose_name='역겨움')),
                ('fear', models.FloatField(blank=True, null=True, verbose_name='두려움')),
                ('happiness', models.FloatField(blank=True, null=True, verbose_name='행복')),
                ('neutral', models.FloatField(blank=True, null=True, verbose_name='중립')),
                ('sadness', models.FloatField(blank=True, null=True, verbose_name='슬픔')),
                ('surprise', models.FloatField(blank=True, null=True, verbose_name='놀람')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('counselor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '영상',
            },
        ),
        migrations.CreateModel(
            name='SentimentGraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='sentiment_graph/')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '꺾은선그래프 - 영상감정',
            },
        ),
    ]
