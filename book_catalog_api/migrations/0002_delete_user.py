# Generated by Django 4.1.2 on 2022-10-12 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_catalog_api', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]