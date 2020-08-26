from django.db import models
from django.db.models import UniqueConstraint


class UserProfile(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    access_permissions = models.CharField(
        max_length=5,
        choices=(("admin", "Administrator"), ("user", "Customer")),
        default="user",
    )

    def __str__(self):
        return self.username

    class Meta:
        constraints = [
            UniqueConstraint(fields=["username"], name="unique_username")
        ]


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    contact_num = models.CharField(max_length=12)
    email_address = models.CharField(max_length=100)
    user_id = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["email_address", "contact_num"], name="unique_contact"
            )
        ]


class CustomerAddress(models.Model):
    cust_add_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    ship_address_line = models.CharField(max_length=100, null=True)
    ship_city = models.CharField(max_length=100, null=True)
    ship_region = models.CharField(max_length=100, null=True)
    ship_country = models.CharField(max_length=100, null=True)
    ship_zip_code = models.CharField(max_length=100, null=True)
    bill_address_line = models.CharField(max_length=100, null=True)
    bill_city = models.CharField(max_length=100, null=True)
    bill_region = models.CharField(max_length=100, null=True)
    bill_country = models.CharField(max_length=100, null=True)
    bill_zip_code = models.CharField(max_length=100, null=True)


class InventoryProduct(models.Model):
    variant_id = models.AutoField(primary_key=True)
    variant_name = models.CharField(max_length=100)
    variant_sku = models.CharField(max_length=100, null=True)
    variant_description = models.CharField(max_length=255, null=True)
    variant_stock = models.IntegerField()
    variant_price = models.FloatField()
    variant_image = models.CharField(
        max_length=1000,
        blank=False,
        default="https://global-uploads.webflow.com/5b44edefca321a1e2d0c2aa6/5c69a7403ca6bd3b0f3600da_Dimensions-Guide-Plants-Indoor-Split-Leaf-Philodendron-Icon.svg",
    )
    variant_is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["variant_sku"], name="unique_sku")
        ]


class Administrator(models.Model):
    admin_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    position = models.CharField(max_length=12)
    email = models.CharField(max_length=100, null=True)
    user_id = models.ForeignKey(UserProfile, on_delete=models.RESTRICT)


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_status = models.CharField(
        max_length=20,
        choices=(("paid", "PAID"), ("unpaid", "UNPAID")),
        default="unpaid",
    )
    payment_date = models.DateField(null=True)
    payment_method = models.CharField(max_length=20, null=True)
    payment_trans_no = models.CharField(max_length=30, null=True)
    payment_amount = models.FloatField(null=True)
    sales_order = models.UUIDField(null=True)


class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    discount_code = models.CharField(max_length=10)
    discount_amount = models.FloatField()


class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    shipment_status = models.CharField(
        max_length=30,
        choices=(
            ("pending_payment", "PENDING PAYMENT"),
            ("waiting_for_confirmation", "CONFIRMING PAYMENT"),
            ("for_shipping", "FOR_SHIPPING"),
            ("shipped", "SHIPPED"),
            ("received", "RECEIVED"),
        ),
        default="pending_payment",
    )
    shipment_courier = models.CharField(
        max_length=20,
        choices=(
            ("lbc", "LBC Express"),
            ("jrs", "JRS Express"),
            ("jnt", "J&T Express"),
            ("mtu", "Meet-up"),
        ),
        null=True,
    )
    shipment_id_url = models.CharField(max_length=100, null=True)
    shipment_date = models.DateField(null=True)
    sales_order = models.UUIDField(null=True)


class SalesOrder(models.Model):
    so_num = models.AutoField(primary_key=True)
    so_trans_no = models.UUIDField(null=True)
    issued_date = models.DateField(auto_now=True)
    total_qty = models.IntegerField()
    total_price = models.FloatField()
    total_tax_amount = models.FloatField()
    total_discount = models.FloatField()
    total_order_amount = models.FloatField()
    payment_status = models.ForeignKey(Payment, on_delete=models.CASCADE)
    shipment_status = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    customer_address = models.ForeignKey(
        CustomerAddress, on_delete=models.CASCADE
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["so_trans_no"], name="unique_so")
        ]


class OrderedProduct(models.Model):
    product_id = models.AutoField(primary_key=True)
    line_item_qty = models.IntegerField()
    line_item_price = models.FloatField()
    variant_name = models.ForeignKey(
        InventoryProduct, on_delete=models.RESTRICT
    )
    customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True
    )
    sales_order_id = models.ForeignKey(
        SalesOrder, on_delete=models.CASCADE, null=True
    )
