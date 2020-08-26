# Generated by Django 3.1 on 2020-08-22 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "plant_shop",
            "0009_administrator_discount_orderedproduct_payment_salesorder_shipment",
        )
    ]

    operations = [
        migrations.AddField(
            model_name="orderedproduct",
            name="customer_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="plant_shop.customer",
            ),
        ),
        migrations.AlterField(
            model_name="salesorder",
            name="issued_date",
            field=models.DateField(auto_now=True),
        ),
    ]
