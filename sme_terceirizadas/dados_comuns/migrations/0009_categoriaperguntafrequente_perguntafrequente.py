# Generated by Django 2.2.8 on 2020-04-22 18:03

import uuid

import django.db.models.deletion
import django_prometheus.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dados_comuns', '0008_auto_20200325_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaPerguntaFrequente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=100, verbose_name='Nome')),
            ],
            bases=(django_prometheus.models.ExportModelOperationsMixin('cat_faq'), models.Model),
        ),
        migrations.CreateModel(
            name='PerguntaFrequente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pergunta', models.TextField(verbose_name='Pergunta')),
                ('resposta', models.TextField(verbose_name='Resposta')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dados_comuns.CategoriaPerguntaFrequente')),
            ],
            bases=(django_prometheus.models.ExportModelOperationsMixin('faq'), models.Model),
        ),
    ]
