# Generated by Django 5.0.4 on 2024-09-23 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuthentificationApp', '0003_remove_produit_boutique'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vente',
            name='total',
        ),
    ]