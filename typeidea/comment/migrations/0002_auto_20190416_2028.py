# Generated by Django 2.2 on 2019-04-16 12:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='target',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='评论目标'),
            preserve_default=False,
        ),
    ]