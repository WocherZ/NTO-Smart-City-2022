# Generated by Django 4.0.2 on 2022-02-18 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_doctor_email_room_is_present'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Название анализа')),
                ('value', models.TextField(verbose_name='Значение анализа')),
            ],
            options={
                'verbose_name': 'Анализ',
                'verbose_name_plural': 'Список анализов',
            },
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={'verbose_name': 'Врач', 'verbose_name_plural': 'Список врачей'},
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'verbose_name': 'Пациент', 'verbose_name_plural': 'Список пациентов'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name': 'Комната', 'verbose_name_plural': 'Комнаты'},
        ),
        migrations.AddField(
            model_name='patient',
            name='height',
            field=models.FloatField(null=True, verbose_name='Рост'),
        ),
        migrations.AddField(
            model_name='patient',
            name='weight',
            field=models.FloatField(null=True, verbose_name='Вес'),
        ),
        migrations.AddField(
            model_name='patient',
            name='analyzes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.analysis', verbose_name='Анализы пациента'),
        ),
    ]
