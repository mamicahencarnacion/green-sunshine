# Generated by Django 3.1 on 2020-08-23 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("plant_shop", "0019_auto_20200823_0147")]

    operations = [
        migrations.AddField(
            model_name="salesorder",
            name="so_trans_no",
            field=models.UUIDField(null=True),
        ),
        migrations.AddConstraint(
            model_name="salesorder",
            constraint=models.UniqueConstraint(
                fields=("so_trans_no",), name="unique_so"
            ),
        ),
    ]
