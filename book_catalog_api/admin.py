from django.contrib import admin
from .models import Books, Authors, Genres, Reviews, Favorites

admin.site.register(Books)
admin.site.register(Authors)
admin.site.register(Genres)
admin.site.register(Reviews)
admin.site.register(Favorites)

