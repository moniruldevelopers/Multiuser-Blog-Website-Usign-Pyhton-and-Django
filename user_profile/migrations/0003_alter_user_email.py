# Generated by Django 4.2.7 on 2023-12-02 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_alter_user_email_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'The email must be unique for create '}, max_length=150, unique=True),
        ),
    ]
