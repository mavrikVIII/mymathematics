# Generated by Django 3.0.2 on 2020-02-04 14:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mathem', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 4, 14, 12, 7, 618853, tzinfo=utc), verbose_name='Дата публикации'),
            preserve_default=False,
        ),
    ]
