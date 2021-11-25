from django.contrib import admin
from .models import BookModels


class AdminBookModels(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'nr_isbn_one', 'nr_isbn_two', 'page_co', 'img_link',
                    'pub_lang')
    list_filter = ('pub_lang',)
    search_fields = ('title',)
    

admin.site.register(BookModels, AdminBookModels)
