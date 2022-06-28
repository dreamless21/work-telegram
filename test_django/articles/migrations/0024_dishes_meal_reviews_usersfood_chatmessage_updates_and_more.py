# Generated by Django 4.0.2 on 2022-06-02 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0023_delete_users_alter_profile_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dishes',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name_dish', models.CharField(max_length=255)),
                ('type_dish', models.IntegerField()),
            ],
            options={
                'db_table': 'dishes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('dt', models.DateField()),
                ('soup_id', models.IntegerField()),
                ('salat_id', models.IntegerField()),
                ('main_id', models.IntegerField()),
                ('garnish_id', models.IntegerField()),
                ('extra_id', models.IntegerField(blank=True, null=True)),
                ('meal_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'db_table': 'meal',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('dt', models.DateField()),
                ('id_user', models.IntegerField()),
                ('id_dish', models.IntegerField()),
                ('rate_dish', models.IntegerField()),
            ],
            options={
                'db_table': 'reviews',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsersFood',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'users_food',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_text', models.TextField()),
                ('dt_send', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Updates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_name', models.CharField(max_length=255)),
                ('desc', models.TextField()),
                ('date_update', models.DateField(auto_now_add=True)),
            ],
        ),
        # migrations.DeleteModel(
        #     name='Users',
        # ),
        migrations.AlterModelOptions(
            name='profile',
            options={'managed': False},
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.profile'),
        ),
    ]