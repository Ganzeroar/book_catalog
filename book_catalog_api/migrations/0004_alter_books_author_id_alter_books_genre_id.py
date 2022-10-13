# Generated by Django 4.1.2 on 2022-10-13 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_catalog_api', '0003_alter_books_publication_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='author_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='book_catalog_api.authors'),
        ),
        migrations.AlterField(
            model_name='books',
            name='genre_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='book_catalog_api.genres'),
        ),
    ]
