# Generated by Django 3.1 on 2020-08-19 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("plant_shop", "0007_inventoryproduct")]

    operations = [
        migrations.AlterField(
            model_name="inventoryproduct",
            name="variant_description",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="inventoryproduct",
            name="variant_sku",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
