from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    id_from_telegram = models.IntegerField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)
    pic = models.TextField(default=None, null=True)
    bio = models.TextField(default=None, null=True)
    city = models.CharField(max_length=255, default=None, null=True)
    phone = models.CharField(max_length=255, default=None, null=True)
    adress = models.CharField(max_length=255, default=None, null=True)
    instagram = models.CharField(max_length=255, default=None, null=True)
    telegram = models.CharField(max_length=255, default=None, null=True)
    facebook = models.CharField(max_length=255, default=None, null=True)
    position = models.CharField(max_length=255, default=None, null=True)
    slug = models.SlugField(unique=True, default=username)

    class Meta:
        db_table = 'profile'
        managed = False

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(Profile, self).save(*args, **kwargs)


class Film(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=9, decimal_places=1, blank=True, null=True)
    pic = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'anime'

    def __str__(self):
        return self.name


class Comment(models.Model):

    comment_text = models.TextField()
    dt_published = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Film, on_delete=models.CASCADE, default=None)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)


    class Meta:
        managed = True
        db_table = 'articles_comments'

    def __str__(self):
        return self.comment_text


class Game(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.SmallIntegerField(default=1)
    dt_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'games'


class Log(models.Model):
    dt = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()
    sys_user = models.CharField(max_length=255)
    json_params = models.JSONField()


class FavoriteFilm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    dt_add = models.DateTimeField(auto_now_add=True)


    class Meta:
        managed = True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Dishes(models.Model):
    id = models.IntegerField(primary_key=True)
    name_dish = models.CharField(max_length=255)
    type_dish = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dishes'


class Meal(models.Model):
    id = models.IntegerField(primary_key=True)
    dt = models.DateField()
    soup_id = models.IntegerField()
    salat_id = models.IntegerField()
    main_id = models.IntegerField()
    garnish_id = models.IntegerField()
    extra_id = models.IntegerField(blank=True, null=True)
    meal_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meal'


class Reviews(models.Model):
    id = models.IntegerField(primary_key=True)
    dt = models.DateField()
    id_user = models.IntegerField()
    id_dish = models.IntegerField()
    rate_dish = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'reviews'


class UsersFood(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users_food'


class Updates(models.Model):
    update_name = models.CharField(max_length=255)
    desc = models.TextField()
    date_update = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'updates_site'


class ChatMessage(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    chat_text = models.TextField()
    dt_send = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_messages'


class Bets(models.Model):
    match_name = models.CharField(max_length=255)
    bet = models.CharField(max_length=255)
    amount = models.IntegerField()
    koef = models.DecimalField(max_digits=19, decimal_places=2)
    result = models.CharField(max_length=255, blank=True, null=True)
    dt = models.DateField()
    total_win = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bets'