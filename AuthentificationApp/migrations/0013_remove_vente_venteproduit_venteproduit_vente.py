# Generated by Django 5.0.4 on 2024-09-27 23:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthentificationApp', '0012_vente_venteproduit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vente',
            name='venteproduit',
        ),
        migrations.AddField(
            model_name='venteproduit',
            name='vente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='AuthentificationApp.vente'),
            preserve_default=False,
        ),
    ]
