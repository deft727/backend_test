# Generated by Django 3.2 on 2021-04-12 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210410_0941'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-pk',)},
        ),
        migrations.AddField(
            model_name='product',
            name='is_popular',
            field=models.BooleanField(default=False, verbose_name='popular?'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(help_text='maximum 500 characters ', max_length=500, verbose_name='Comment'),
        ),
    ]
