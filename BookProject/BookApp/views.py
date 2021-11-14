import requests
import json
import re
from django.shortcuts import render, reverse, get_object_or_404, HttpResponseRedirect, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
from .models import BookModels
from .forms import BookAddForm, BookFilterForm, ContactForm
from .filters import BookFilter
import collections
from django.conf import settings


# Strona główna z pocztą z portfolio
def base(request):
    if request.method == 'POST':  # Czy formularz zostal wyslany od klienta na serwer
        form = ContactForm(request.POST)  # Formularz z wypelniona trescia
        if form.is_valid():  # Sprawdzamy walidacje tych pol z formularza. Jezeli zawartosc ma true, wykonuje ifa.
            ''' Rozpocznamy weryfikację reCAPTCHA '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY_BASE,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' Kończymy weryfikację reCAPTCHA '''

            cd = form.cleaned_data
            admin_adres = 'django4everpl@gmail.com'  # Adres na ktory zostanie wyslany mail od klienta
            responder_adres = 'django4everpl@gmail.com'  # Adres z ktorego bedzie wyslana wiadomosc do klienta
            client_adres = request.POST['email']
            sub = "Wiadomość od PortSG.PL"
            message_for_admin = """
            Imię użytkownika: {}
            Adres e-mail: {}

            Treść zapytania: {}
            """.format(cd['name'], client_adres, cd['message'])
            message_for_client = """
            Witaj, {}
            dziękuje za wyslanie wiadomosci. 

            Odpowiem najszybciej jak to mozliwe :)

            Wiadomosc została wygenerowana automatycznie,
            proszę na nią nie odpowiadać.

            Kłaniam się i pozdrawiam.
            PortSG.pl

            Dane kontakowe:
            Sebastian Grabarczyk
            Tel. 724-309-198
            E-mail: Najlepiej pisać na rec@interia.eu
            E-mail: django4everpl@gmail.com
            """.format(cd['name'])
            try:
                if result['success']:
                    send_mail(sub, message_for_admin, responder_adres, [admin_adres, ])
                    send_mail(sub, message_for_client, responder_adres, [client_adres, ])
                    messages.success(request, 'Wysłano twoją wiadomość e-mail! Odezwę się naszybciej jak to możliwe :)')
                else:
                    form = ContactForm()
                    messages.error(request, 'Potwierdz że nie jesteś Robotem!')
                # Wyslanie maila do klienta z trescia atuomatyczna
            except BadHeaderError:  # Sprawdza czy nie ma próby iniekcji kodu
                print("Wykryto nieprawidłowy nagłówek")
                form = ContactForm()
                messages.error(request, 'Coś poszło nie tak. Spróbuj jeszcze raz!')
                data['info'] = 'Dziekuje za wyslanie wiadomosci'

    else:
        form = ContactForm()  # Jezeli zadna wiadomosc nie zostala wyslana na serwer to generujemy formularz
    return render(request, 'BookApp/base.html', {'form': form})


# Pobieranie kluczy
def get_by_keys(res, *keys):
    try:
        for k in keys:
            res = res[k]
        return res
    except (TypeError, KeyError, IndexError):
        return None


# Import książek
def book_api_views(request):
    book_import = []

    if request.method == 'POST':
        filter_ch = BookFilterForm(request.POST)
        if filter_ch.is_valid():
            cd = filter_ch.cleaned_data

            filter_choice = cd['choose_v']
            filter_search = cd['search']

            search_url = "https://www.googleapis.com/books/v1/volumes?"

            params = {
                'q': '{}{}'.format(filter_choice, filter_search),
                'key': settings.BOOK_DATA_API_KEY,
                'maxResults': 8,
                'printType': 'books'

            }

            r = requests.get(search_url, params=params)
            results = r.json()['items']

            for result in results:

                book_data = {
                    'title': get_by_keys(result, 'volumeInfo', 'title'),
                    'authors': get_by_keys(result, 'volumeInfo', 'authors', 0),
                    'publish_date': get_by_keys(result, 'volumeInfo', 'publishedDate'),
                    'isbn_one': get_by_keys(result, 'volumeInfo', 'industryIdentifiers', 0, 'identifier'),
                    'isbn_two': get_by_keys(result, 'volumeInfo', 'industryIdentifiers', 1, 'identifier'),
                    'page_count': get_by_keys(result, 'volumeInfo', 'pageCount'),
                    'thumbinail': get_by_keys(result, 'volumeInfo', 'imageLinks', 'thumbnail'),
                    'country': get_by_keys(result, 'volumeInfo', 'language')
                }

                book_import.append(book_data)

                
                # Wyciąganie daty i rozbijanie, niestety nie wiem jeszcze jak dodać do DateField, kiedy 
                # występuje tylko sam rok lub rok z datą. Poniżej kod z przykładową datą.
                # date_n= '2022-12-25'
                # year_pattern = r'(?P<year>\d{4})'
                # month_pattern = r"(?:-(?P<month>\d{1,2}))"
                # day_pattern = r"(?:-(?P<day>\d{1,2}))"
                # match_date = re.search(rf'{year_pattern}(?:{month_pattern}{day_pattern}?)?', date_n)
                # 
                # year_n = match_date.group('year')
                # month_n = match_date.group('month')
                # day_n = match_date.group('day')
                # 
                # print("OSOBNE: ", year_n, month_n, day_n)
                # 
                # if year_n and month_n and day_n:
                #     a = "{}.{}.{}".format(day_n, month_n, year_n)
                #     print(a)
                # elif year_n and month_n:
                #     b = "{}.{}".format(month_n, year_n)
                #     print(b)
                # elif year_n:
                #     c = "{}".format(year_n)
                #     print(c)
                # else:
                #     print("Brak daty")
                
                # # Zapisywanie w bazie
                # title = get_by_keys(result, 'volumeInfo', 'title')
                # author = get_by_keys(result, 'volumeInfo', 'authors', 0)
                # nr_isbn_one = get_by_keys(result, 'volumeInfo', 'industryIdentifiers', 0, 'identifier')
                # nr_isbn_two = get_by_keys(result, 'volumeInfo', 'industryIdentifiers', 1, 'identifier'),
                # page_co = get_by_keys(result, 'volumeInfo', 'pageCount')
                # img_link = get_by_keys(result, 'volumeInfo', 'imageLinks', 'thumbnail')
                # pub_lang = get_by_keys(result, 'saleInfo', 'country')
                #
                # book_data_save = BookModels(
                #     title=title,
                #     author=author,
                #     nr_isbn_one=nr_isbn_one,
                #     nr_isbn_two=nr_isbn_two,
                #     data_publikacji=None,
                #     numer_ISBN=222,
                #     page_co=page_co,
                #     img_link=img_link,
                #     pub_lang=pub_lang,
                # )
                # book_data_save.save()

    else:
        filter_ch = BookFilterForm()
    return render(request, "BookApp/book_import.html", {'book_import': book_import,
                                                        'filter_ch': filter_ch})


# Filtrowanie pozycji dla tabeli z książkami
def book_filter_views(request):
    book_list = BookModels.objects.all()
    my_filter = BookFilter(request.GET, queryset=book_list)
    book_list = my_filter.qs

    return render(request, 'BookApp/book_table.html', {'book_list': book_list,
                                                       'my_filter': my_filter})


# Szczegóły książki
def book_detail_views(request, pid, slug, author, year):
    det = get_object_or_404(BookModels, id=pid, slug=slug, author=author, pub_date__year=year)
    return render(request, 'BookApp/book_detail.html', {'det': det,
                                                        })


# Dodawanie książki
def book_add_views(request):
    if request.method == 'POST':  # Czy formularz zostal wyslany od klienta na serwer
        form = BookAddForm(request.POST)  # Formularz z wypelniona trescia
        if form.is_valid():
            form.save()
            return redirect('BookApp:book_table')
    else:
        form = BookAddForm()
    return render(request, 'BookApp/book_add.html', {
        'form': form
    })


# Aktualizacje pozycji
class BookUpdateView(UpdateView):
    # specify the model you want to use
    model = BookModels

    fields = [
        "title",
        "author",
        "pub_date",
        "nr_isbn_one",
        "nr_isbn_two",
        "page_co",
        "img_link",
        "pub_lang"
    ]

    template_name = 'BookApp/book_update.html'

    def get_success_url(self):
        return reverse('BookApp:book_table')


# Kaswowanie pozycji z tabeli
def book_delete_views(request, pk):
    if request.method == 'POST':
        book = BookModels.objects.get(pk=pk)
        book.delete()
    return redirect('BookApp:book_table')
