# Generated by Django 5.0.1 on 2024-01-10 11:22

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('food', '0001_initial'),
        ('restaurant', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(default='f9c7c2b98a344d65a3aeebe330e91210', editable=False, max_length=100, unique=True)),
                ('review', models.DecimalField(decimal_places=1, default=0, max_digits=3, validators=[django.core.validators.MaxValueValidator(5.0)])),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('registration_time', models.DateTimeField(auto_now=True)),
                ('delivery_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('CP', 'Complete'), ('UC', 'UpComing'), ('CN', 'Canceled')], default='UC', max_length=500)),
                ('credit_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.card')),
                ('delivery_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.address')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.food')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('discount', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
