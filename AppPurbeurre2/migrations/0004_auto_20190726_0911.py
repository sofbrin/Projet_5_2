# Generated by Django 2.2.3 on 2019-07-26 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppPurbeurre2', '0003_auto_20190723_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorydb',
            name='url',
            field=models.CharField(default=' ', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productdb',
            name='origin',
            field=models.TextField(),
        ),
    ]
