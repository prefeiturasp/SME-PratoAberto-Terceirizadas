# Generated by Django 2.0.13 on 2019-07-16 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0007_remove_diretoriaregional_iniciais'),
        ('cardapio', '0006_auto_20190716_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='suspensaoalimentacao',
            name='escola',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='escola.Escola'),
            preserve_default=False,
        ),
    ]