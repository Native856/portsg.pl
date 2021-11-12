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


def create_book(id, tytul, autor, numer_ISBN, liczba_stron, link_do_okladki, jezyk_publikacji):
    date_c = datetime.date.today()
    return BookModels.objects.create(id=id,
                                         tytul=tytul,
                                         autor=autor,
                                         data_publikacji=date_c,
                                         numer_ISBN=numer_ISBN,
                                         liczba_stron=liczba_stron,
                                         link_do_okladki=link_do_okladki,
                                         jezyk_publikacji=jezyk_publikacji)


# Tworzymy nowy wpis w bazie i sprawdzamy czy poprawnie jest zwracany
class CreateReportTest(unittest.TestCase):
    def setUp(self):
        self.new_book = create_book(id=1,
                                    tytul='Hobbit',
                                    autor='J. R. R. Tolkien',
                                    numer_ISBN=8381162645,
                                    liczba_stron=304,
                                    link_do_okladki=None,
                                    jezyk_publikacji='PL')

    def testReturn(self):
        self.assertEqual(self.new_book.__str__(), 'Tytul książki TEST Hobbit')


# Tworzymy w bazie wpis ksiazki i sprawdzamy go znajduje sie pod adresem book_table
class BaseContentTest(TestCase):
    def testContent(self):
        # Podobnie jak w shellu przypisujemy pod response konkretny url
        # self.assertEqual(response.status_code, 200)  # Sprawdza czy status jest rowny 200
        cb = create_book(id=1,
                         tytul='Hobbit',
                         autor='J. R. R. Tolkien',
                         numer_ISBN=8381162645,
                         liczba_stron=304,
                         link_do_okladki=None,
                         jezyk_publikacji='PL'
        response = self.client.get(reverse('BookApp:book_table'))
        self.assertContains(response, cb.tytul)
        # Sprawdza, czy zawiera liste z tytułem Hobbit
        self.assertQuerysetEqual(response.context["book_list"], ['<BookModelsTest: Tytuł książki Hobbit>'])

                         
class TestUrls(TestCase):
    def test_urls_base(self):
        url = reverse('BookApp:base')
        print(resolve(url))
        # print pokazuje dostepne func
        # Sprawdzamy, czy wywołując resolve z "BaseSG:base" znajduje funkcję o nazwie base.
        self.assertEquals(resolve(url).func, base)
