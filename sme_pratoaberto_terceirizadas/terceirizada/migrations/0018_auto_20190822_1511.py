# Generated by Django 2.0.13 on 2019-08-22 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terceirizada', '0017_terceirizada_usuarios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='edital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contratos', to='terceirizada.Edital'),
        ),
    ]
