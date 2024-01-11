# Generated by Django 5.0.1 on 2024-01-10 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('food', '0002_alter_food_category'),
        ('restaurant', '0002_alter_restaurant_background_pic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='fav_foods',
            field=models.ManyToManyField(blank=True, to='food.food'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fav_restaurant',
            field=models.ManyToManyField(blank=True, to='restaurant.restaurant'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
