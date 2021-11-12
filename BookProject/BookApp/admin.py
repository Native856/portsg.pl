from django.contrib import admin
from .models import BookModels


class AdminBookModels(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'nr_isbn_one', 'nr_isbn_two', 'page_co', 'img_link',
                    'pub_lang')


admin.site.register(BookModels, AdminBookModels)
