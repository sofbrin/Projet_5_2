# Generated by Django 2.2.3 on 2019-07-23 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppPurbeurre2', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdb',
            name='url',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]