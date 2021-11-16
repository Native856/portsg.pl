from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField

# Model książki
class BookModels(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name='Tytuł')
    slug = AutoSlugField(populate_from='title')
    author = models.CharField(max_length=200, verbose_name='Autor')
    pub_date = models.DateField(null=True, blank=True, verbose_name='Data publikacji')
    nr_isbn_one = models.IntegerField(verbose_name='Pierwszy ISBN')
    nr_isbn_two = models.IntegerField(blank=True, null=True, verbose_name='Drugi ISBN')
    page_co = models.IntegerField(verbose_name='Ilość stron')
    img_link = models.CharField(max_length=200, null=True, blank=True, verbose_name='Link do okładki')
    pub_lang = models.CharField(max_length=20, verbose_name='Język publikacji (wpisz: PL lub EN)')

    def __str__(self):
        return "Tytuł książki {}".format(self.title)

    def get_absolute_url(self):
        return reverse('BookApp:book_detail',
                       args=[self.id,
                             self.slug,
                             self.pub_date.year])

    class Meta:
        verbose_name = 'Książki'
        verbose_name_plural = 'Dodaj książkę'
