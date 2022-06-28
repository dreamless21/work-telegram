from django import forms
from .models import Dishes
CHOICES = [
    (50, 50), (100, 100), (150, 150)
]

CARD_CHOICES = [
    ('Black', 'Черный'), ('Red', 'Красный'), ('Diamonds', 'Бубы'), ('Hearts', "Черви"), ('Clubs', "Трефы"), ('Spades', "Пики")
]


soup_choices = [(0, 'Выберите суп из меню')] + [(choice.pk, choice.name_dish) for choice in Dishes.objects.filter(type_dish=1).order_by('name_dish')]
salat_choices = [(0, 'Выберите салат из меню')] + [(choice.pk, choice.name_dish) for choice in Dishes.objects.filter(type_dish=2).order_by('name_dish')]
main_choices = [(0, 'Выберите второе блюдо из меню')] + [(choice.pk, choice.name_dish) for choice in Dishes.objects.filter(type_dish=3).order_by('name_dish')]
garnish_choices = [(0, 'Выберите гарнир из меню')] + [(choice.pk, choice.name_dish) for choice in Dishes.objects.filter(type_dish=4).order_by('name_dish')]


rates = [(0, 'Выберите оценку для блюда')] + [(i, i) for i in range(1, 6)]


class SearchingForm(forms.Form):
    searching = forms.CharField(widget=forms.TextInput)


class UserRegistration(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'last name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'confirm password'}))


class UserAuth(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'username',
                                                             'id': 'floatingInput'}), label='UsErNaMe')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'password'}), label='PaSsWoRd')


class Comments(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 60%; height: '
                                                                                           '100px; margin: 10px;'}))


class Playing(forms.Form):
    choice = forms.ChoiceField(choices=(('Even', 'Чётный'), ('Odd', 'Нечётный')), widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 30%; height: '
                                                                                           '35px; margin: 10px;'}))
    bet = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 30%; height: '
                                                                                           '35px; margin: 10px;'}))


class PlayCards(forms.Form):
    type_bet = forms.ChoiceField(choices=CARD_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 30%; height: '
                                                                                           '35px; margin: 10px;'}))


class Menu(forms.Form):
    soup = forms.ChoiceField(choices=soup_choices, widget=forms.Select(attrs={'class': 'form-select'}))
    soup_rate = forms.ChoiceField(choices=rates, widget=forms.Select(attrs={'class': 'form-select'}))
    salat = forms.ChoiceField(choices=salat_choices, widget=forms.Select(attrs={'class': 'form-select'}))
    salat_rate = forms.ChoiceField(choices=rates, widget=forms.Select(attrs={'class': 'form-select'}))
    main = forms.ChoiceField(choices=main_choices, widget=forms.Select(attrs={'class': 'form-select'}))
    main_rate = forms.ChoiceField(choices=rates, widget=forms.Select(attrs={'class': 'form-select'}))
    garnish = forms.ChoiceField(choices=garnish_choices, widget=forms.Select(attrs={'class': 'form-select'}))
    garnish_rate = forms.ChoiceField(choices=rates, widget=forms.Select(attrs={'class': 'form-select'}))
    #dt = forms.ChoiceField(widget=forms.DateInput(attrs={'class': 'form-select'}))
