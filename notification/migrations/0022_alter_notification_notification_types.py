# Generated by Django 4.2.7 on 2023-12-06 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0021_alter_notification_notification_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_types',
            field=models.CharField(choices=[('Like', 'Like'), ('Follow', 'Follow'), ('Blog', 'Blog')], max_length=20),
        ),
    ]
