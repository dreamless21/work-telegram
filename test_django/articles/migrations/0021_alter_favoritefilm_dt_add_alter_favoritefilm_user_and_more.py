# Generated by Django 4.0.2 on 2022-05-24 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0020_alter_favoritefilm_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritefilm',
            name='dt_add',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='favoritefilm',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        # migrations.DeleteModel(
        #     name='Users',
        # ),
    ]
