# Generated by Django 2.0.13 on 2019-07-10 18:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('escola', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descricao')),
                ('nome', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome')),
                ('ativo', models.BooleanField(default=True, verbose_name='Está ativo?')),
                ('data_inicial', models.DateField(verbose_name='Data inicial')),
                ('data_final', models.DateField(verbose_name='Data final')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Lote',
                'verbose_name_plural': 'Lotes',
            },
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iniciais', models.CharField(blank=True, max_length=10, null=True, verbose_name='Iniciais')),
                ('nome', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('diretoria_regional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='lotes', to='escola.DiretoriaRegional')),
            ],
            options={
                'verbose_name': 'Lote',
                'verbose_name_plural': 'Lotes',
            },
        ),
        migrations.CreateModel(
            name='Terceirizada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True, verbose_name='Está ativo?')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nome_fantasia', models.CharField(max_length=160, verbose_name='Nome fantasia')),
                ('cnpj', models.CharField(max_length=14, validators=[django.core.validators.MinLengthValidator(14)], verbose_name='CNPJ')),
                ('lotes', models.ManyToManyField(to='terceirizada.Lote')),
            ],
            options={
                'verbose_name': 'Terceirizada',
                'verbose_name_plural': 'Terceirizadas',
            },
        ),
    ]