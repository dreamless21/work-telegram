# Generated by Django 4.0.2 on 2022-06-02 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0027_alter_comment_options'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='comment',
        #     name='article',
        #     field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='articles.film'),
        # ),
        migrations.AddField(
            model_name='comment',
            name='dt_deleted',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='is_deleted',
            field=models.SmallIntegerField(default=0),
        ),
    ]