# Generated by Django 2.1.3 on 2022-06-07 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0003_auto_20220606_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='upload_method',
            field=models.CharField(max_length=20, null=True, verbose_name='Upload Method'),
        ),
    ]