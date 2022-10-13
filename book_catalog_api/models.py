from django.db import models
from django.db.models import IntegerField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


class Genres(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Authors(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Books(models.Model):
    name = models.CharField(max_length=100)
    genre_id = models.ForeignKey(
        Genres,
        on_delete=models.PROTECT,
    )
    author_id = models.ForeignKey(
        Authors,
        on_delete=models.PROTECT,
    )
    publication_date = models.DateField()
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    @classmethod
    def get_filtered_data(cls, request_data):
        books = Books.objects.all()
        genre_name = request_data.get('genre')
        author_name = request_data.get('author')
        date_from = request_data.get('date_from')
        date_to = request_data.get('date_to')

        if genre_name:
            genre_id = Genres.objects.get(name__contains=genre_name)
            books = books.filter(genre_id=genre_id)
        if author_name:
            author_id = Authors.objects.get(name__contains=author_name)
            books = books.filter(author_id=author_id)
        if date_from:
            books = books.filter(publication_date__gte=date_from)
        if date_to:
            books = books.filter(publication_date__lte=date_to)
        return books


class Reviews(models.Model):
    book = models.ForeignKey(
        Books,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    raiting = IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
    )
    review_text = models.CharField(max_length=1000)

    def __str__(self):
        return self.review_text


class Favorites(models.Model):
    book = models.ForeignKey(
        Books,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
