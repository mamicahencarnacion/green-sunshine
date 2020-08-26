# Generated by Django 3.1 on 2020-08-22 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("plant_shop", "0017_administrator_email")]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="payment_amount",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="payment",
            name="payment_method",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="payment",
            name="payment_trans_no",
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="shipment",
            name="shipment_courier",
            field=models.CharField(
                choices=[
                    ("lbc", "LBC Express"),
                    ("jrs", "JRS Express"),
                    ("jnt", "J&T Express"),
                    ("mtu", "Meet-up"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="shipment",
            name="shipment_date",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="shipment",
            name="shipment_id_url",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="shipment",
            name="shipment_status",
            field=models.CharField(
                choices=[
                    ("pending_payment", "PENDING PAYMENT"),
                    ("for_shipping", "FOR_SHIPPING"),
                    ("shipped", "SHIPPED"),
                    ("received", "RECEIVED"),
                ],
                default="pending_payment",
                max_length=30,
            ),
        ),
    ]