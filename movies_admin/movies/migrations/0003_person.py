# Generated by Django 4.2.5 on 2024-02-06 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_film_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='gender',
            field=models.TextField(choices=[('male', 'male'), ('famale', 'female')], null=True, verbose_name='gender'),
        ),
    ]
