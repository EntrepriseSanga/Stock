# Generated by Django 5.0.4 on 2024-10-18 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthentificationApp', '0020_credits_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='est_super',
            field=models.BooleanField(default=False),
        ),
    ]