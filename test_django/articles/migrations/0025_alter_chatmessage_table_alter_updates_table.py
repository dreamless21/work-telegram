# Generated by Django 4.0.2 on 2022-06-02 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0024_dishes_meal_reviews_usersfood_chatmessage_updates_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='chatmessage',
            table='chat_messages',
        ),
        migrations.AlterModelTable(
            name='updates',
            table='updates_site',
        ),
    ]