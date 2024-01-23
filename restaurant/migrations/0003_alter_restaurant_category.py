# Generated by Django 5.0.1 on 2024-01-23 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_alter_restaurant_background_pic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='category',
            field=models.CharField(choices=[('IT', 'Italian'), ('CH', 'Chicken'), ('AS', 'Asian'), ('DS', 'Dessert'), ('BU', 'Burger'), ('FI', 'Fish'), ('PI', 'Pizza')], max_length=30),
        ),
    ]
