# Generated by Django 5.0.4 on 2024-10-18 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuthentificationApp', '0021_utilisateur_est_super'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='est_super',
        ),
    ]