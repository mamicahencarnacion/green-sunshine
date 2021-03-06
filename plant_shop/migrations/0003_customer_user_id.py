# Generated by Django 3.1 on 2020-08-18 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("plant_shop", "0002_customer")]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="user_id",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.RESTRICT,
                to="plant_shop.userprofile",
            ),
            preserve_default=False,
        )
    ]
