# Generated by Django 2.0.13 on 2019-08-07 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0005_auto_20190807_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subprefeitura',
            name='lote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subprefeituras', to='escola.Lote'),
        ),
    ]
