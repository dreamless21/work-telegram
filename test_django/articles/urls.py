from django.urls import path, include
from .views import FilmView, full_list, main_page, play, registration, auth, profile, log_out, menu_choice, detail_upgrade, play_dice, play_cards, test, my_bets
from django.views.generic.base import RedirectView

app_name = 'articles'

urlpatterns = [
    path('api/', FilmView.as_view()),
    path('home/', main_page, name='home'),
    path('', RedirectView.as_view(url='home/')),
    path('articles/<int:article_id>/', detail_upgrade, name="show-article"),
    path('articles/', full_list, name='articles'),
    path('playing/', play, name="playing"),
    path('reg/', registration, name='reg'),
    path('auth/', auth, name='auth'),
    path('profile/<slug:slug>/', profile, name='profile'),
    path('logout/', log_out, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('menu/', menu_choice, name='menu'),
    path('playing/dice/', play_dice, name='dice'),
    path('playing/cards/', play_cards, name='cards'),
    path('test1/', test),
    path('bets/', my_bets, name='bets')
]