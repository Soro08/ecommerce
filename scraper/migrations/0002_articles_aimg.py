# Generated by Django 2.2.1 on 2019-05-12 21:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='aimg',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]