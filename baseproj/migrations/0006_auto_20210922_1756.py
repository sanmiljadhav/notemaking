# Generated by Django 3.1.4 on 2021-09-22 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseproj', '0005_auto_20210922_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharedwith',
            name='note_desc',
            field=models.TextField(default='SOME STRING'),
        ),
        migrations.AddField(
            model_name='sharedwith',
            name='note_title',
            field=models.CharField(default='SOME STRING', max_length=100),
        ),
    ]
