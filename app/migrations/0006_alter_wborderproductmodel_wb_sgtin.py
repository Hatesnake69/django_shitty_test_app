# Generated by Django 5.1.3 on 2024-11-16 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_wborderproductmodel_wb_sgtin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wborderproductmodel',
            name='wb_sgtin',
            field=models.CharField(blank=True, default=None, max_length=256, null=True),
        ),
    ]