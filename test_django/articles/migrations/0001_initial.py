# Generated by Django 4.0.2 on 2022-05-04 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=9)),
                ('pic', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
    ]
