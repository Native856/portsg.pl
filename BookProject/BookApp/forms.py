from django import forms
from .models import BookModels


class BookAddForm(forms.ModelForm):
    class Meta:
        model = BookModels
        fields = ('title', 'author', 'pub_date', 'nr_isbn_one', 'nr_isbn_two', 'page_co', 'img_link', 'pub_lang')
        widgets = {
            'pub_date': forms.DateInput(format=('%m/%d/%Y'),
                                        attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                               'type': 'date'})}


class BookFilterForm(forms.Form):
    FILTER = [
        ('intitle:', 'Tytuł'),
        ('inauthor:', 'Autor'),
        ('inpublisher:', 'Wydawca'),
        ('subject:', 'Przedmiot'),
        ('isbn:', 'isbn:'),
        ('lccn:', 'Nr. Kontrolny'),
        ('oclc:', 'Centrum bibl. komp.'),
    ]
    choose_v = forms.ChoiceField(label='Filtruj:', choices=FILTER)
    search = forms.CharField(label='Wpisz to czego szukasz', max_length=100)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=20, label="Twoje Imię: ")
    email = forms.EmailField(label="Twoj adres e-mail: ")
    message = forms.CharField(label="Wiadomość: ", widget=forms.Textarea)
