# Generated by Django 4.1.7 on 2023-03-09 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('butcher_shop_app', '0011_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('my_id', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_processed', models.BooleanField(default=False)),
                ('user_phone', models.CharField(max_length=20)),
                ('comment', models.TextField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_count', models.PositiveIntegerField()),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='butcher_shop_app.order')),
                ('product_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='butcher_shop_app.product')),
            ],
        ),
    ]