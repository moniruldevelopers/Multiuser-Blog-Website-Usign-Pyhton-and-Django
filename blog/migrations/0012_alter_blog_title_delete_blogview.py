# Generated by Django 4.2.7 on 2023-12-27 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_blogview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=250, unique=True),
        ),
        migrations.DeleteModel(
            name='BlogView',
        ),
    ]
