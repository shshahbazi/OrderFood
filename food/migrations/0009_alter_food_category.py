# Generated by Django 5.0.1 on 2024-01-26 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0008_alter_food_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='category',
            field=models.CharField(choices=[('PI', 'Pizza'), ('AS', 'Asian'), ('FI', 'Fish'), ('CH', 'Chicken'), ('IT', 'Italian'), ('BU', 'Burger'), ('DS', 'Dessert')], default='AS', max_length=30),
        ),
    ]
