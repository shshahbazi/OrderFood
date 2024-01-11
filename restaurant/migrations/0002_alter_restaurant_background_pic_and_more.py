# Generated by Django 5.0.1 on 2024-01-10 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='background_pic',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='category',
            field=models.CharField(choices=[('AS', 'Asian'), ('BU', 'Burger'), ('PI', 'Pizza'), ('CH', 'Chicken'), ('DS', 'Dessert'), ('FI', 'Fish'), ('IT', 'Italian')], max_length=30),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='features',
            field=models.ManyToManyField(blank=True, to='restaurant.restaurantfeature'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='icon',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
