# Generated by Django 2.1 on 2018-08-14 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sal', '0004_auto_20180814_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicearea',
            name='polygon',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='servicearea',
            name='x1',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='servicearea',
            name='x2',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='servicearea',
            name='y1',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='servicearea',
            name='y2',
            field=models.FloatField(default=0),
        ),
        migrations.AddIndex(
            model_name='servicearea',
            index=models.Index(fields=['-x1'], name='sal_service_x1_abb381_idx'),
        ),
        migrations.AddIndex(
            model_name='servicearea',
            index=models.Index(fields=['-y1'], name='sal_service_y1_9a084e_idx'),
        ),
        migrations.AddIndex(
            model_name='servicearea',
            index=models.Index(fields=['x2'], name='sal_service_x2_eaffc8_idx'),
        ),
        migrations.AddIndex(
            model_name='servicearea',
            index=models.Index(fields=['y2'], name='sal_service_y2_6c3065_idx'),
        ),
    ]
