# Generated by Django 3.0.2 on 2020-02-04 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mathem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=50, verbose_name='Имя автора комментария')),
                ('comment_text', models.CharField(max_length=200, verbose_name='Текст комментария')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mathem.Question')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]