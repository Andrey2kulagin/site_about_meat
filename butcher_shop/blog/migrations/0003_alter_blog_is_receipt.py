# Generated by Django 4.1.7 on 2023-03-09 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_is_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='is_receipt',
            field=models.BooleanField(default=False),
        ),
    ]
