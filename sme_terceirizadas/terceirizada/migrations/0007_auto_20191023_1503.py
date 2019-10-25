# Generated by Django 2.2.6 on 2019-10-23 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0007_auto_20191023_1503'),
        ('terceirizada', '0006_auto_20191008_1819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='terceirizada',
            name='usuarios',
        ),
        migrations.AddField(
            model_name='terceirizada',
            name='vinculos',
            field=models.ManyToManyField(blank=True, related_name='terceirizadas', to='perfil.Vinculo'),
        ),
    ]