# Generated by Django 2.0.13 on 2019-05-22 22:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MealKit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=160, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
            ],
            options={
                'verbose_name': 'Meal Kit',
                'verbose_name_plural': 'Meal Kits',
            },
        ),
        migrations.CreateModel(
            name='OrderMealKit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=160, verbose_name='Order Location')),
                ('students_quantity', models.IntegerField(verbose_name='Students Quantity')),
                ('order_date', models.DateField(verbose_name='Order Date')),
                ('observation', models.TextField(blank=True, null=True, verbose_name='Observation')),
                ('status', models.CharField(choices=[('SAVED', 'SALVO'), ('SENDED', 'ENVIADO'), ('CANCELED', 'CANCELADO'), ('DENIED', 'NEGADO')], default=0, max_length=6, verbose_name='Status')),
                ('scheduled_time', models.CharField(max_length=60, verbose_name='Scheduled Time')),
                ('register', models.DateTimeField(auto_now_add=True, verbose_name='Registered')),
                ('meal_kits', models.ManyToManyField(to='meal_kit.MealKit')),
            ],
            options={
                'verbose_name': 'Solicitar Kit Lanche',
                'verbose_name_plural': 'Solicitar Kits Lanche',
            },
        ),
    ]
