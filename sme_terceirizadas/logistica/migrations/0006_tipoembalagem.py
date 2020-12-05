# Generated by Django 2.2.13 on 2020-11-30 16:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('logistica', '0005_solicitacaoremessa_distribuidor'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoEmbalagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('sigla', models.CharField(max_length=10, verbose_name='Código')),
                ('descricao', models.CharField(max_length=100, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Tipo de Emabalgem Fechada',
                'verbose_name_plural': 'Tipos de Emabalgens Fechadas',
            },
        ),
    ]