# Generated by Django 4.0.5 on 2022-07-11 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_gender_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='accounts/avatar/%Y/%m/%d'),
        ),
    ]
