# Generated by Django 5.0.3 on 2024-03-16 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_grocerylist_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grocerylist',
            name='items',
            field=models.ManyToManyField(to='app.groceryitem'),
        ),
    ]
