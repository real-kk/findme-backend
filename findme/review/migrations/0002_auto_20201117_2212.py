# Generated by Django 3.1.2 on 2020-11-17 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]