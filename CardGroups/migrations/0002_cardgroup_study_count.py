# Generated by Django 3.2.9 on 2021-11-26 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CardGroups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardgroup',
            name='study_count',
            field=models.IntegerField(default=0),
        ),
    ]