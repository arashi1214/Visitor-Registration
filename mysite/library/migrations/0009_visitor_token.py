# Generated by Django 3.2.5 on 2021-07-21 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_visitor_is_acitve'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='token',
            field=models.CharField(default='', max_length=500),
        ),
    ]
