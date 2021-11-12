import requests
from django.shortcuts import render, reverse, get_object_or_404, HttpResponseRedirect, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
from .models import BookModels, BookTest, Meal, BookModelsTest
from .forms import BookAddForm, BookFilterForm
import json
from .filters import BookFilter

import collections

from django.conf import settings

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from BookApp.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# Strona główna
def base(request):
    return render(request, 'BookApp/base.html')


def get_by_keys(res, *keys):
    try:
        for k in keys:
            res = res[k]
            print("PIERWSZA RES:", res)
        return res
    except (TypeError, KeyError, IndexError):
        return None




def BookAPI(request):
    book_import = []

    if request.method == 'POST':
        filter_ch = BookFilterForm(request.POST)
        if filter_ch.is_valid():
            cd = filter_ch.cleaned_data

            filter_choice = cd['choose_v']
            filter_search = cd['search']

            search_url = "https://www.googleapis.com/books/v1/volumes?"

            choose = 'inauthor:'

            params = {
                'q': '{}{}'.format(filter_choice, filter_search),
                'key': settings.BOOK_DATA_API_KEY,
                'maxResults': 3,
                'printType': 'books'

            }

            r = requests.get(search_url, params=params)

            # print(r.json()['items'][0]['id'])
            # print(r.json()['items'])

            results = r.json()['items']


            for result in results:

                # book_data = {
                #     'title': result['volumeInfo']['title'],
                #     # 'title': get_by_keys(result, 'volumeInfo', 'title'),
                #     # 'authors': result['volumeInfo']['authors'][0],
                #     'authors': get_by_keys(result, 'volumeInfo', 'authors', 0),
                #     'publish_date': result['volumeInfo']['publishedDate'],
                #     'isbn_one': result['volumeInfo']['industryIdentifiers'],
                #     # 'isbn_one': result['volumeInfo']['industryIdentifiers'][0:]['identifier'],
                #     # 'isbn_two': result['volumeInfo']['industryIdentifiers'][1]['identifier'],
                #     'page_count': result['volumeInfo']['pageCount'],
                #     # 'thumbinail': result['volumeInfo']['imageLinks']['thumbnail'],
                #     'country': result['saleInfo']['country']
                # }
                # book_exists_thumbinail = {
                #     'thumbinail': result['volumeInfo']['imageLinks']['thumbnail']
                # }
                # book_import.append(book_exists_thumbinail)


                book_data = {
                    'title': get_by_keys(result, 'volumeInfo', 'title'),
                    'authors': get_by_keys(result, 'volumeInfo', 'authors', 0),
                    'publish_date': get_by_keys(result, 'volumeInfo', 'publishedDate'),
                    # 'isbn_one': get_by_keys(result, 'volumeInfo', 'industryIdentifiers', 0, 'identifier'),
                    # 'isbn_one_two': get_by_keys(result, 'volumeInfo', 'industryIdentifiers', 1, 'identifier'),
                    # 'isbn_one': result['volumeInfo']['industryIdentifiers'][0:]['identifier'],
                    # 'isbn_two': result['volumeInfo']['industryIdentifiers'][1]['identifier'],
                    'page_count': get_by_keys(result, 'volumeInfo', 'pageCount'),
                    'thumbinail': get_by_keys(result, 'volumeInfo', 'imageLinks', 'thumbnail'),
                    'country': get_by_keys(result, 'saleInfo', 'country')
                }

                print(get_by_keys(result, 'volumeInfo', 'industryIdentifiers', 0, 'identifier'))

                print("Zawartosc book_data:", book_data)
                book_import.append(book_data)

                # bb = result['volumeInfo']['imageLinks']['thumbnail'] in book_data
                # Z takimi danymi wejsciowymi zawsze zmienne beda mialy None wiec wykona tylko else
                # th = result['volumeInfo'].get('imageLinks')
                # # rr = result.get('volumeInfo', {}).get('imageLinks', {}).get('thumbnail')
                # # isbn_zr = result.get('volumeInfo', {}).get('industryIdentifiers', {}).get('')
                #
                # # print("ZERO:", isbn_zr)
                #
                # # isbn_zero = result['volumeInfo']['industryIdentifiers'][1].get('identifier')
                # isbn_zer = result['volumeInfo']['industryIdentifiers']
                #
                # print('CALA LISTA:', book_data)
                #
                # print("DANE WYJSCIOWE:", isbn_zer)
                #
                # dic = collections.defaultdict(list)
                #
                #
                # for d in isbn_zer:
                #     for k, v in d.items():
                #         dic[k].append(v)

                #
                # # Musi byc petla zeby sprawdzic po elementach iterowac
                #
                # try:
                #     dic = collections.defaultdict(list)
                #
                #     for d in isbn_zer:
                #         for k, v in d.items():
                #             dic[k].append(v)
                #     print("DIC WYJSCIOWY:", dic)
                #
                #     book_exists_isbn = {
                #         'isbn_two': dic['identifier']
                #     }
                #
                #     dnew_isbn = {**book_data, **book_exists_isbn}
                #     book_import.append(dnew_isbn)
                #     print("DIC OK")
                #
                #     book_exists_thumbinail = {
                #         'thumbinail': result['volumeInfo']['imageLinks']['thumbnail']
                #     }
                #
                #     dnew = {**book_data, **book_exists_thumbinail}
                #     book_import.append(dnew)
                #     print("TH OK")
                # except KeyError:
                #     print("Zły klucz")
                #

                # DWA POPRAWNE IFY
                # if isbn_zer is not None:
                #     book_exists_isbn = {
                #         'isbn_two': dic['identifier']
                #     }
                #
                #     dnew_isbn = {**book_data, **book_exists_isbn}
                #     book_import.append(dnew_isbn)
                #     print("DIC OK")
                # else:
                #     book_exists_isbn_n = {
                #         'isbn_two': None
                #     }
                #
                #     dnew_none_isbn = {**book_data, **book_exists_isbn_n}
                #     book_import.append(dnew_none_isbn)
                #     print("DIC N-OK")
                #
                # if th is not None:
                #     book_exists_thumbinail = {
                #         'thumbinail': result['volumeInfo']['imageLinks']['thumbnail']
                #     }
                #
                #     dnew = {**book_data, **book_exists_thumbinail}
                #     book_import.append(dnew)
                #     print("TH OK")
                #
                # else:
                #     book_exists_thumbinail_n = {
                #         'thumbinail': None
                #     }
                #
                #     dnew_none = {**book_data, **book_exists_thumbinail_n}
                #     book_import.append(dnew_none)
                #     print("TH N-OK")
                # if dic is not None:
                #     book_exists_isbn = {
                #         'isbn_two': dic['identifier']
                #     }
                #
                #     dnew_isbn = {**book_data, **book_exists_isbn}
                #
                #     print("IF od ISBN:", dnew_isbn)
                #
                #     book_import.append(dnew_isbn)
                #     print("WARUNEK OK")
                # else:
                #     book_exists_isbn_n = {
                #         'isbn_two': None
                #     }
                #
                #     dnew_none_isbn = {**book_data, **book_exists_isbn_n}
                #
                #     book_import.append(dnew_none_isbn)

                # isb = json.loads(request.POST.get('identifier'))

                # print("LOAD:", isb)
                # isbn = isbn_zero.get('identifier')
                #
                # print("Pobieranie ISBN", isbn)
                # cr = book_data.get('page_count')


                # # Poprawnie dziala dla pobierania IMG lub dodania None
                # if th is not None:
                #     book_exists_thumbinail = {
                #         'thumbinail': result['volumeInfo']['imageLinks']['thumbnail']
                #     }
                #
                #     dnew = {**book_data, **book_exists_thumbinail}
                #
                #     book_import.append(dnew)
                #
                #     print("WARUNEK OK IMG")
                #
                # else:
                #     book_exists_thumbinail_n = {
                #         'thumbinail': None
                #     }
                #
                #     dnew_none = {**book_data, **book_exists_thumbinail_n}
                #
                #     book_import.append(dnew_none)
                #
                #     print("WARUNEK NIE OK OD IMG")
                #
                #     print("WARUNEK NIE OK")

                # else:
                #     book_exists_thumbinail_n = {
                #         'thumbinail': None
                #     }
                #
                #     dnew_none = {**book_data, **book_exists_thumbinail_n}
                #
                #     book_import.append(dnew_none)
                #
                #     print("WARUNEK NIE OK OD IMG")

                # if isbn_zero is not None:
                #     book_exists_isbn = {
                #         'isbn_two': result['volumeInfo']['industryIdentifiers'][1]['identifier']
                #     }
                #
                #     dnew_isbn = {**book_data, **book_exists_isbn}
                #
                #     print("IF od ISBN:", dnew_isbn)
                #
                #     book_import.append(dnew_isbn)
                #
                # else:
                #     book_exists_isbn_n = {
                #         'isbn_two': None
                #     }
                #
                #     dnew_none_isbn = {**book_data, **book_exists_isbn_n}
                #
                #     book_import.append(dnew_none_isbn)

                # if cc is not None:
                #     book_exists_isbn_two = {
                #         'isbn_two': result['volumeInfo']['industryIdentifiers'][1]['identifier'],
                #     }
                #
                #     book_import.append(book_exists_isbn_two)
                # else:
                #     book_exists_isbn_two_not = {
                #         'isbn_two': None
                #     }
                #
                #     book_import.append(book_exists_isbn_two_not)
                #
                # if cr is not None:
                #     book_exists_page_count = {
                #         'page_count': result['volumeInfo']['pageCount']
                #     }
                #
                #     book_import.append(book_exists_page_count)
                # else:
                #     book_exists_page_count_not = {
                #         'page_count': None
                #     }
                #
                #     book_import.append(book_exists_page_count_not)


                # # Zapisywanie w bazie
                # title = get_by_keys(result, 'volumeInfo', 'title')
                # author = get_by_keys(result, 'volumeInfo', 'authors', 0)
                # page_count = get_by_keys(result, 'volumeInfo', 'pageCount')
                # link_to_img = get_by_keys(result, 'volumeInfo', 'imageLinks', 'thumbnail')
                # pub_lang = get_by_keys(result, 'saleInfo', 'country')
                #
                # book_data_save = BookModelsTest(
                #     tytul=title,
                #     autor=author,
                #     data_publikacji=None,
                #     numer_ISBN=222,
                #     liczba_stron=page_count,
                #     link_do_okladki=link_to_img,
                #     jezyk_publikacji=pub_lang,
                # )
                # book_data_save.save()


    else:
        filter_ch = BookFilterForm()
    return render(request, "BookApp/book_import.html", {'book_import': book_import,
                                                        'filter_ch': filter_ch})


def BookTestViews(request):
    all_books = {}
    if 'title_name' in request.GET:
        name = request.GET['title_name']
        url = 'https://www.googleapis.com/books/v1/volumes?q={}'.format(name)
        response = requests.get(url)
        data = response.json()
        book = data['items']

        # Petla dla szukanych obiektów wiec w zdjeciu tez musi byc slowo lub litera
        for q in book:
            book_data = BookTest(
                title_book=q['volumeInfo']['title'],
                authors=q['volumeInfo']['authors'],
                image=q['volumeInfo']['imageLinks']['thumbnail'],
            )
            book_data.save()
            all_books = BookTest.objects.all().order_by('-id')

    return render(request, 'BookApp/book_test.html', {"all_books": all_books})


def get_meals(request):
    all_meals = {}
    if 'name' in request.GET:
        name = request.GET['name']
        url = 'https://www.themealdb.com/api/json/v1/1/search.php?s=%s' % name
        response = requests.get(url)
        data = response.json()
        meals = data['meals']

        for i in meals:
            meal_data = Meal(
                name=i['strMeal'],
                category=i['strCategory'],
                instructions=i['strInstructions'],
                region=i['strArea'],
                slug=i['idMeal'],
                image_url=i['strMealThumb']
            )
            meal_data.save()
            all_meals = Meal.objects.all().order_by('-id')

    return render(request, 'BookApp/meal.html', {"all_meals": all_meals})


def meal_detail(request, id):
    meal = Meal.objects.get(id=id)
    print(meal)
    return render(request, 'BookApp/meal_detail.html', {'meal': meal})


def BookListViews(request):
    response = requests.get('https://api.github.com/events')
    return render(request, 'BookApp/book_list.html', {'response': response})


# def get_book(request, car_name):
#     if request.method == 'GET':
#         try:
#             car = BookModels.objects.get(title=tytul)
#             response = json.dumps([{ 'title': car.name}])
#         except:
#             response = json.dumps([{ 'Error': 'No car with that name'}])
#     return HttpResponse(response, content_type='text/json')
#
# @csrf_exempt
# def add_book(request):
#     if request.method == 'POST':
#         payload = json.loads(request.body)
#         car_name = payload['car_name']
#         top_speed = payload['top_speed']
#         car = Car(name=car_name, top_speed=top_speed)
#         try:
#             car.save()
#             response = json.dumps([{ 'Success': 'Car added successfully!'}])
#         except:
#             response = json.dumps([{ 'Error': 'Car could not be added!'}])
#     return HttpResponse(response, content_type='text/json')


def BookTest_Views(request):
    book_list = BookModelsTest.objects.all()
    myFilter = BookFilter(request.GET, queryset=book_list)
    book_list = myFilter.qs

    return render(request, 'BookApp/book_table.html', {'book_list': book_list,
                                                       'myFilter': myFilter, })


def book_detail_Views(request, deti, tytul, autor, day, month, year):
    det = get_object_or_404(BookModelsTest, id=deti,
                            tytul=tytul,
                            autor=autor,
                            data_publikacji__day=day,
                            data_publikacji__month=month,
                            data_publikacji__year=year)
    return render(request, 'BookApp/book_detail.html', {'det': det,
                                                        })


def book_add_Views(request):
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


class BookUpdateView(UpdateView):
    # specify the model you want to use
    model = BookModelsTest

    # specify the fields
    fields = [
        "tytul",
        "autor",
        "data_publikacji",
        "numer_ISBN",
        "liczba_stron",
        "link_do_okladki",
        "jezyk_publikacji"
    ]
    template_name = 'BookApp/book_update.html'

    def get_success_url(self):
        return reverse('BookApp:book_table')


def BookDeleteView(request, pk):
    if request.method == 'POST':
        book = BookModelsTest.objects.get(pk=pk)
        book.delete()
    return redirect('BookApp:book_table')
