import uuid

from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import SimpleTemplateResponse
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection


import random
import requests
import json
import datetime


from .models import Film, Comment, FavoriteFilm, Profile, Bets
from .serializers import FilmSerializer
from .forms import SearchingForm, UserRegistration, UserAuth, Comments, Playing, PlayCards, Menu, soup_choices, salat_choices, main_choices, garnish_choices, rates
from .static_package import card_dict


class FilmView(APIView):
    def get(self, request):
        articles = Film.objects.all()
        serializer = FilmSerializer(articles, many=True)
        return Response({'films': serializer.data})


@login_required
def full_list(request):
    film_list = Film.objects.all()
    template = loader.get_template('articles/full_list.html')
    context = {
        'film_list': film_list,
        'title': 'Catalog'
    }

    return HttpResponse(template.render(context, request))


# def show_article(request, article_id):
#     article = get_object_or_404(Film, pk=article_id)
#     template = loader.get_template('articles/detail.html')
#     in_favorite = FavoriteFilm.objects.filter(film=article, user=request.user, is_deleted=0)
#     form = Comments()
#     if request.POST.get('favorite'):
#         action = request.POST.get('favorite')
#         if action == 'add':
#             try_to_find = FavoriteFilm.objects.get(user=request.user, film=article, is_deleted=1)
#             if try_to_find:
#                 try_to_find.is_deleted = 0
#                 try_to_find.dt_deleted = None
#                 try_to_find.save()
#             else:
#                 FavoriteFilm.objects.create(user=request.user, film=article)
#         elif action == 'delete':
#             article_delete = FavoriteFilm.objects.get(user=request.user, film=article)
#             article_delete.is_deleted = 1
#             article_delete.dt_deleted = datetime.datetime.now()
#             article_delete.save()
#     elif request.POST.get('delete-button'):
#         comment_id = request.POST.get('delete-button')
#         Comment.objects.filter(id=comment_id).delete()
#     elif request.method == 'POST':
#         form = Comments(request.POST)
#         if form.is_valid():
#             text = form.cleaned_data['text']
#             Comment.objects.create(author_name=request.user.username, comment_text=text, article=article,
#             author=request.user)
#             form = Comments()
#     comments = Comment.objects.select_related('author').filter(article=article).order_by('-dt_published')
#     context = {
#         'article': article,
#         'form': form,
#         'comments': comments,
#         'title': article.name,
#         'in_fav': in_favorite
#     }
#     return HttpResponse(template.render(context, request))


def main_page(request):
    template = loader.get_template('articles/index.html')
    context = {
        'title': 'Home'
    }
    return HttpResponse(template.render(context, request))


# region Playing
@login_required
def play(request):
    template = loader.get_template('play/playing.html')
    context = {
        'title': 'Gaming'
    }
    return HttpResponse(template.render(context, request))


def play_cards(request):
    template = loader.get_template('play/cards.html')
    if request.method == 'POST':
        form = PlayCards(request.POST)
        if form.is_valid():
            type_bet = request.POST['type_bet']
            msg, card_value, card_image, card_suit = card_round(type_bet, request)
            context = {
                'title': 'PlayZone',
                'card': card_value,
                'card_image': card_image,
                'message': msg,
                'balance': request.user.profile.balance
            }

            return HttpResponse(template.render(context, request))

    else:
        form = PlayCards()

    context = {
            'form_card': form
        }

    return HttpResponse(template.render(context, request))


def card_round(type_bet, request):
    deck_id = json.loads(requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)[
        'deck_id']
    draw_card = \
        json.loads(requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1').text)['cards'][0]
    card_code, card_image, card_suit = draw_card['code'], draw_card['image'], draw_card['suit']
    trans_id, bet = uuid.uuid4(), 150
    card_proc(-1, request.user.id, trans_id, 3, bet, type_bet, card_code)
    if card_suit in card_dict[type_bet][0]:
        card_proc(1, request.user.id, trans_id, 3, bet * card_dict[type_bet][1], type_bet, card_code)
        flag = 'Win'
    else:
        flag = 'Loose'
    return flag, card_code, card_image, card_suit


def card_proc(move, user_id, trans_id, game_id, amount, type_bet, card_value):
    cursor = connection.cursor()
    args = [user_id, trans_id, game_id, amount, type_bet, card_value]
    if move == -1:
        cursor.callproc('Cards_payIn', args)
    elif move == 1:
        args = args[:-2]
        cursor.callproc('Cards_payOut', args)

    return None


def play_dice(request):
    template = loader.get_template('play/dice.html')
    if request.method == 'POST':
        form = Playing(request.POST)
        if form.is_valid():
            user_id = request.user.id
            bet = int(form.cleaned_data['bet'])
            trans_id = uuid.uuid4()
            dice_num = random.randint(1, 6)
            user_choice = form.cleaned_data['choice']
            dice_proc(user_id, -1, trans_id, bet, user_choice, dice_num)
            msg = 'Loose'
            if (dice_num % 2 == 1 and user_choice == 'Odd') or (dice_num % 2 == 0 and user_choice == 'Even'):
                dice_proc(user_id, 1, trans_id, bet * 2)
                msg = 'Win'
            context = {
                'title': 'PlayZone',
                'user_name': request.user.profile.username,
                'balance': request.user.profile.balance,
                'number': dice_num,
                'msg': msg
            }

            return HttpResponse(template.render(context, request))

    else:
        form = Playing()

    context = {
        'title': 'PlayZone',
        'form': form
    }
    return HttpResponse(template.render(context, request))


def dice_proc(user_id, move, trans_id, bet, user_choice=None, dice_num=None):
    cursor = connection.cursor()
    game_id = 1
    args = [user_id, trans_id, game_id, bet]
    bets = {
        'Odd': 4,
        'Even': 3
    }
    if move == -1:
        args.extend([bets[user_choice], dice_num])
        cursor.callproc('Dice_payIn', args)
    elif move == 1:
        cursor.callproc('Dice_payOut', args)

    return None
# endregion


# region User login
def registration(request):
    template = loader.get_template('registration/registration.html')
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            if password == confirm_password:
                User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
                message = 'You are register'

            else:
                message = 'Passwords don\'t match'
            context = {
                'message': message,
                'title': 'Registration'
            }
            return HttpResponse(template.render(context, request))

    form = UserRegistration()
    context = {
        'form': form,
        'title': 'Registration'
    }
    return HttpResponse(template.render(context, request))


def auth(request):
    template = loader.get_template('registration/login.html')
    next_page = request.POST.get('next', None)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if next_page:
                return HttpResponseRedirect(next_page)
            else:
                return HttpResponseRedirect('/articles/')
        else:
            message = 'Something went wrong'
        context = {
            'message': message,
            'title': 'Authorisation'
            }
        return HttpResponse(template.render(context, request))

    form = UserAuth()
    context = {
        'form': form,
        'title': 'Authorisation'
    }
    return HttpResponse(template.render(context, request))


@login_required
def profile(request, slug):
    user_profile = Profile.objects.get(slug=slug)
    template = loader.get_template('registration/profile.html')
    fav_films = Film.objects.filter(id__in=FavoriteFilm.objects.filter(user_id=user_profile.user_id).values('film_id'))
    comments = Comment.objects.filter(author_id=user_profile.user_id)
    context = {
        'user_pr': user_profile,
        'fav_films': fav_films,
        'comments': comments
    }
    return HttpResponse(template.render(context, request))


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/home/')
# endregion


def menu_choice(request):
    if request.method == 'POST':
        form = Menu(request.POST)
        if form.is_valid():
            msg = dbmenu_proc(form, request)
            return HttpResponse(msg)
        else:
            return HttpResponse('error')

    template = loader.get_template('articles/food.html')
    form = Menu()
    context = {
        'title': 'Menu',
        'form': form,
        'fields': [soup_choices, rates, salat_choices, rates,  main_choices, rates, garnish_choices, rates]
    }
    return HttpResponse(template.render(context, request))


def dbmenu_proc(form, request):
    soup, soup_rate = form.cleaned_data['soup'], form.cleaned_data['soup_rate']
    salat, salat_rate = form.cleaned_data['salat'], form.cleaned_data['salat_rate']
    main, main_rate = form.cleaned_data['main'], form.cleaned_data['main_rate']
    garnish, garnish_rate = form.cleaned_data['garnish'], form.cleaned_data['garnish_rate']
    dt = datetime.date.today()
    user_id = request.user.id
    args = [user_id, dt, soup, soup_rate, salat, salat_rate, main, main_rate, garnish, garnish_rate]
    cursor = connection.cursor()
    cursor.callproc('web_main_obed_proc', args)

    return 'Success'


def detail_upgrade(request, article_id):
    article = get_object_or_404(Film, pk=article_id)
    template = loader.get_template('articles/new_detail.html')
    in_favorite = FavoriteFilm.objects.filter(film=article, user=request.user)
    form = Comments()
    if request.POST.get('favorite'):
        action = request.POST.get('favorite')
        if action == 'add':
            FavoriteFilm.objects.create(user=request.user, film=article)
        elif action == 'delete':
            FavoriteFilm.objects.get(user=request.user, film=article).delete()
    elif request.POST.get('delete-button'):
        comment_id = request.POST.get('delete-button')
        Comment.objects.filter(id=comment_id).delete()
    elif request.method == 'POST':
        form = Comments(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            Comment.objects.create(comment_text=text, article=article,
                                   author_id=request.user.id)
            form = Comments()
    comments = Comment.objects.select_related('author').filter(article=article).order_by('-dt_published')
    context = {
        'article': article,
        'form': form,
        'comments': comments,
        'title': article.name,
        'in_fav': in_favorite
    }
    return HttpResponse(template.render(context, request))


def test():
    return SimpleTemplateResponse(loader.get_template('articles/test_bootstrap.html'))


def my_bets(request):
    template = loader.get_template('articles/bets.html')
    bets = Bets.objects.all().order_by('dt', 'id')
    context = {
        'title': 'bets',
        'bets': bets
    }

    return HttpResponse(template.render(context, request))
