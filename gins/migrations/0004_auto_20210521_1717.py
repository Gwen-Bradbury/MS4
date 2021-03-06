# Generated by Django 3.2 on 2021-05-21 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gins', '0003_alter_gincategory_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gin',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to=''),
        ),
        migrations.AlterField(
            model_name='gin',
            name='image_url',
            field=models.URLField(blank=True, default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='gin',
            name='sku',
            field=models.CharField(blank=True, default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='gincategory',
            name='friendly_name',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
