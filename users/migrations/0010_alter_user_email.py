# Generated by Django 3.2.9 on 2021-11-17 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=100, null=True, unique=True),
        ),
    ]