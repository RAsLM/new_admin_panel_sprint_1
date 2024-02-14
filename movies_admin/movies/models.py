import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Now


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(_('created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)
    creation_date = models.DateTimeField(default=Now(), null=True, blank=True)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(_('type'), max_length=255)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    certificate = models.CharField(_('certificate'), null=True, max_length=512, blank=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        indexes = [
            models.Index(fields=['creation_date'], name='film_work_creation_date_idx'),
        ]

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        unique_together = ('film_work', 'genre',)
        db_table = "content\".\"genre_film_work"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанрыы'


class Gender(models.TextChoices):
    MALE = 'male', _('male')
    FEMALE = 'famale', _('female')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)
    persons = models.ManyToManyField(Filmwork, through='PersonFilmwork')
    gender = models.TextField(_('gender'), choices=Gender.choices, null=True)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), null='true', default='actor')
    created_at = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        unique_together = ('film_work', 'person', )
        indexes = [
            models.Index(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_idx'),
        ]
