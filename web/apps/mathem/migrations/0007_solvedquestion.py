# Generated by Django 3.0.2 on 2020-02-14 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mathem', '0006_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolvedQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('people', models.CharField(max_length=200, verbose_name='Имя решившего задачу')),
                ('solved_question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mathem.Question')),
            ],
            options={
                'verbose_name': 'Решенная задача',
                'verbose_name_plural': 'Решенные задачи',
            },
        ),
    ]