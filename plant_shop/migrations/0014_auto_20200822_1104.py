# Generated by Django 3.1 on 2020-08-22 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("plant_shop", "0013_auto_20200822_1100")]

    operations = [
        migrations.AlterField(
            model_name="inventoryproduct",
            name="variant_image",
            field=models.CharField(
                default="https://www.pngkey.com/png/full/7-73059_28-collection-of-plant-drawing-png-yellow-tumblr.png",
                max_length=1000,
            ),
        )
    ]
