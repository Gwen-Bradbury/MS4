# Generated by Django 3.2 on 2021-04-30 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('blog', '0002_auto_20210421_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment_author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_author',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment', to='profiles.userprofile'),
        ),
        migrations.AddField(
            model_name='post',
            name='post_user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='profiles.userprofile'),
        ),
    ]
