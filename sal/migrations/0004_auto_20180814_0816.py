# Generated by Django 2.1 on 2018-08-14 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sal', '0003_servicearea_provider'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servicearea',
            options={'ordering': ('provider', 'name')},
        ),
        migrations.AlterField(
            model_name='servicearea',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='servicearea',
            unique_together={('provider', 'name')},
        ),
    ]
