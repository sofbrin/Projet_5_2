# Generated by Django 2.2.3 on 2019-07-15 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryDb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProductDb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('origin', models.CharField(max_length=255)),
                ('manufacturing_places', models.CharField(max_length=255)),
                ('countries', models.CharField(max_length=255)),
                ('store', models.CharField(max_length=255)),
                ('nutriscore', models.CharField(max_length=5)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppPurbeurre2.CategoryDb')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricDb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_original', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_original', to='AppPurbeurre2.ProductDb')),
                ('product_replaceable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_replaceable', to='AppPurbeurre2.ProductDb')),
            ],
        ),
    ]
