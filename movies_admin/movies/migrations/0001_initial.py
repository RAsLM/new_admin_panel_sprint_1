# Generated by Django 4.2.5 on 2024-02-14 18:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.datetime
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('creation_date', models.DateTimeField(blank=True, default=django.db.models.functions.datetime.Now(), null=True)),
                ('rating', models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='rating')),
                ('type', models.CharField(max_length=255, verbose_name='type')),
                ('certificate', models.CharField(blank=True, max_length=512, null=True, verbose_name='certificate')),
                ('file_path', models.FileField(blank=True, null=True, upload_to='movies/', verbose_name='file')),
            ],
            options={
                'verbose_name': 'Фильм',
                'verbose_name_plural': 'Фильмы',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('full_name', models.CharField(max_length=255, verbose_name='full_name')),
                ('gender', models.TextField(choices=[('male', 'male'), ('famale', 'female')], null=True, verbose_name='gender')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.TextField(default='actor', null='true', verbose_name='role')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.person')),
            ],
            options={
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmwork', to='movies.filmwork'),
        ),
        migrations.CreateModel(
            name='GenreFilmwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('film_work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.genre')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанрыы',
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.GenreFilmwork', to='movies.genre'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='personfilmwork',
            unique_together={('film_work', 'person')},
        ),
        migrations.AlterUniqueTogether(
            name='genrefilmwork',
            unique_together={('film_work', 'genre')},
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['creation_date'], name='film_work_creation_date_idx'),
        ),
    ]