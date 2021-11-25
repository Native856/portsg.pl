from django.test import TestCase
import unittest
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from BookApp.models import BookModels
from django.urls import reverse, resolve
from BookApp.views import base
from django.utils import timezone
import datetime
from datetime import date
from django.test.client import Client


# Sprawdzamy czy mamy dostep do strony głównej
class ResponseTest(TestCase):
    def test_details(self):
        response = self.client.get(reverse('BookApp:base'))
        self.failUnlessEqual(response.status_code, 200)


def create_book(id, title, author, slug, nr_isbn_one, nr_isbn_two, page_co, img_link, pub_lang):
    date_c = datetime.date.today()
    return BookModels.objects.create(id=id,
                                     title=title,
                                     author=author,
                                     slug=slug,
                                     pub_date=date_c,
                                     nr_isbn_one=nr_isbn_one,
                                     nr_isbn_two=nr_isbn_two,
                                     page_co=page_co,
                                     img_link=img_link,
                                     pub_lang=pub_lang)


# Tworzymy nowy wpis w bazie i sprawdzamy czy poprawnie jest zwracany
class CreateReportTest(unittest.TestCase):
    def setUp(self):
        self.new_book = create_book(id=1,
                                    title='Hobbit',
                                    author='J. R. R. Tolkien',
                                    slug='hobbit',
                                    nr_isbn_one=8381162645,
                                    nr_isbn_two=3443242,
                                    page_co=304,
                                    img_link=None,
                                    pub_lang='pl')

    def testReturn(self):
        self.assertEqual(self.new_book.__str__(), 'Tytuł książki Hobbit')


# Tworzymy w bazie wpis ksiazki i sprawdzamy go znajduje sie pod adresem book_table
class BaseContentTest(TestCase):
    def testContent(self):
        # Podobnie jak w shellu przypisujemy pod response konkretny url
        # self.assertEqual(response.status_code, 200)  # Sprawdza czy status jest rowny 200
        cb = create_book(id=1,
                         title='Hobbit',
                         author='J. R. R. Tolkien',
                         slug='hobbit',
                         nr_isbn_one=8381162645,
                         nr_isbn_two=3443242,
                         page_co=304,
                         img_link=None,
                         pub_lang='pl')
        # Sprawdzamy, czy na stronie głownej znajduje sie wpis "Brak opisu.", jeżeli opis nie został dodany.
        # self.assertContains(response, 'Hobbit')
        response = self.client.get(reverse('BookApp:book_table'))
        self.assertContains(response, cb.title)
        # Sprawdza, czy zawiera pustą liste dla opisu desc
        self.assertQuerysetEqual(response.context["book_list"], ['<BookModels: Tytuł książki Hobbit>'])


class TestUrls(TestCase):
    def test_urls_base(self):
        url = reverse('BookApp:base')
        print(resolve(url))
        # print pokazuje dostepne func
        # Sprawdzamy, czy wywołując resolve z "BaseSG:base" znajduje funkcję o nazwie base.
        self.assertEquals(resolve(url).func, base)
