# Generated by Django 2.2.9 on 2020-01-14 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200113_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='path',
            field=models.TextField(null=True, unique=True),
        ),
    ]
