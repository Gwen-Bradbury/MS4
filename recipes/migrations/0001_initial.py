# Generated by Django 3.2 on 2021-04-18 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('friendly_name', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'verbose_name_plural': 'Recipe Categories',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('name', models.CharField(max_length=254)),
                ('ingredients', models.TextField()),
                ('method', models.TextField()),
                ('garnish', models.TextField()),
                ('recipecategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.recipecategory')),
            ],
        ),
    ]
