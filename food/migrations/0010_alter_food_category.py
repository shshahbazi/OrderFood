# Generated by Django 5.0.1 on 2024-01-26 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0009_alter_food_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='category',
            field=models.CharField(choices=[('DS', 'Dessert'), ('AS', 'Asian'), ('FI', 'Fish'), ('PI', 'Pizza'), ('IT', 'Italian'), ('BU', 'Burger'), ('CH', 'Chicken')], default='AS', max_length=30),
        ),
    ]
