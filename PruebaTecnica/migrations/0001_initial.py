# Generated by Django 4.1 on 2023-02-14 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('horario', models.CharField(max_length=60)),
                ('fechaInicio', models.DateField()),
                ('fechaFin', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'curso',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('apellido', models.CharField(max_length=100)),
                ('edad', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'db_table': 'estudiante',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='DetalleInscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PruebaTecnica.curso')),
                ('estudiante', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PruebaTecnica.estudiante')),
            ],
            options={
                'db_table': 'detalle_inscripcion',
                'managed': True,
            },
        ),
    ]
