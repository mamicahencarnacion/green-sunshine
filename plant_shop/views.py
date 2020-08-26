import base64
import uuid

import requests
from django.shortcuts import render

from plant_shop.models import (
    UserProfile,
    Customer,
    CustomerAddress,
    InventoryProduct,
    OrderedProduct,
    SalesOrder,
    Administrator,
    Payment,
    Shipment,
)

DEFAULT_IMAGE = "https://global-uploads.webflow.com/5b44edefca321a1e2d0c2aa6/5c69a7403ca6bd3b0f3600da_Dimensions-Guide-Plants-Indoor-Split-Leaf-Philodendron-Icon.svg"


def index(request):
    context = {
        "products": InventoryProduct.objects.filter(variant_is_active=True),
        "access": request.session.get("access"),
    }

    if request.session.has_key("username"):
        context.update({"username": request.session["username"]})

        if request.session.get("access") == "admin":
            user = UserProfile.objects.get(
                username=request.session["username"]
            )
            admin = Administrator.objects.get(user_id=user)
            return render(request, "admin_dashboard.html", {"profile": admin})

    return render(request, "index.html", context)


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def profile(request):
    if request.session.has_key("username"):
        user = UserProfile.objects.get(username=request.session["username"])
        customer = Customer.objects.get(user_id=user)
        context = {
            "user": user,
            "customer": customer,
            "access": request.session["access"],
        }
        try:
            customer_address = CustomerAddress.objects.get(
                customer_id=customer
            )
            context.update({"customer_address": customer_address})
        except CustomerAddress.DoesNotExist:
            pass

        return render(request, "profile.html", context=context)
    return render(request, "unauthorized.html")


def order_form(request):
    context = None
    if request.session.has_key("username"):
        username = request.session["username"]
        user = UserProfile.objects.get(username=username)
        customer = Customer.objects.get(user_id=user)
        try:
            customer_address = CustomerAddress.objects.get(
                customer_id=customer
            )
        except CustomerAddress.DoesNotExist:
            return render(
                request, "update_shipping.html", {"customer": customer}
            )
        context = {
            "username": username,
            "user": user,
            "customer": customer,
            "customer_address": customer_address,
            "products": InventoryProduct.objects.filter(
                variant_is_active=True
            ),
        }
    return render(request, "order_form.html", context)


def product_details(request, pk):
    product = InventoryProduct.objects.get(variant_id=pk)

    context = {"product": product}

    if request.session.has_key("access") and request.session.has_key(
        "username"
    ):
        context.update(
            {
                "access": request.session["access"],
                "username": request.session["username"],
            }
        )
    return render(request, "products_details.html", context=context)


def shipping(request, pk):
    customer = Customer.objects.get(customer_id=pk)
    context = {"customer": customer}
    try:
        customer_address = CustomerAddress.objects.get(customer_id=customer)
        context.update({"customer_address": customer_address})
    except CustomerAddress.DoesNotExist:
        pass

    return render(request, "update_shipping.html", context=context)


def billing(request, pk):
    customer = Customer.objects.get(customer_id=pk)
    return render(
        request,
        "update_billing.html",
        {"customer_id": pk, "customer": customer},
    )


def register_new_user(request):
    if request.method == "POST":
        post_request = request.POST
        password = post_request["password"]

        encoded_password = base64.b64encode(
            bytes(f"{password}-{password}".encode())
        ).decode()

        user_profile = UserProfile(
            username=post_request["username"], password=encoded_password
        )
        user_profile.save()

        customer_details = Customer(
            first_name=post_request["first_name"],
            last_name=post_request["last_name"],
            contact_num=f"63{post_request['contact_num']}",
            email_address=post_request["email_address"],
            user_id=user_profile,
        )
        customer_details.save()

        return render(request, "success.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            return render(request, "unauthorized.html")

        encoded_password = base64.b64encode(
            bytes(f"{password}-{password}".encode())
        ).decode()

        if user and user.password == encoded_password:
            request.session["username"] = user.username
            request.session["access"] = user.access_permissions
            if user.access_permissions == "admin":
                try:
                    admin = Administrator.objects.get(user_id=user)
                except Administrator.DoesNotExist:
                    return render(request, "login.html")

                return render(
                    request, "admin_dashboard.html", {"profile": admin}
                )

            # customer = Customer.objects.get(user_id=user.user_id)
            # try:
            #     customer_address = CustomerAddress.objects.get(
            #         customer_id=customer.customer_id
            #     )
            # except CustomerAddress.DoesNotExist:
            #     customer_address = None

            return render(
                request,
                "index.html",
                {
                    "username": request.session["username"],
                    "products": InventoryProduct.objects.filter(
                        variant_is_active=True
                    ),
                    "access": user.access_permissions,
                },
            )


def update_shipping(request, pk):
    if request.method == "POST":
        request_details = request.POST
        try:
            customer_address = CustomerAddress.objects.get(customer_id=pk)
            customer = Customer.objects.get(customer_id=pk)
            print(request_details)

            if customer_address:
                customer_address.ship_address_line = request_details[
                    "address_line"
                ]
                customer_address.ship_city = request_details["city"]
                customer_address.ship_region = request_details["region"]
                customer_address.ship_zip_code = request_details["zip"]
                customer_address.ship_country = (
                    request_details.get("country") or "Philippines"
                )

                if request_details.get("same-as-billing"):
                    customer_address.bill_address_line = request_details[
                        "address_line"
                    ]
                    customer_address.bill_city = request_details["city"]
                    customer_address.bill_region = request_details["region"]
                    customer_address.bill_zip_code = request_details["zip"]
                    customer_address.bill_country = (
                        request_details.get("country") or "Philippines"
                    )

                customer_address.save()

                return render(
                    request,
                    "profile.html",
                    {
                        "customer": customer,
                        "customer_address": customer_address,
                    },
                )

        except CustomerAddress.DoesNotExist:
            customer = Customer.objects.get(customer_id=pk)
            customer_address = CustomerAddress(
                customer_id=customer,
                ship_address_line=request_details["address_line"],
                ship_city=request_details["city"],
                ship_region=request_details["region"],
                ship_zip_code=request_details["zip"],
                ship_country=request_details.get("country") or "Philippines",
            )

            if request_details.get("same-as-billing"):
                customer_address.bill_address_line = request_details[
                    "address_line"
                ]
                customer_address.bill_city = request_details["city"]
                customer_address.bill_region = request_details["region"]
                customer_address.bill_zip_code = request_details["zip"]
                customer_address.bill_country = (
                    request_details.get("country") or "Philippines"
                )

            customer_address.save()

            return render(
                request,
                "profile.html",
                {"customer": customer, "customer_address": customer_address},
            )


def update_billing(request, pk):
    if request.method == "POST":
        request_details = request.POST
        try:
            customer_address = CustomerAddress.objects.get(customer_id=pk)
            customer = Customer.objects.get(customer_id=pk)

            if customer_address:
                customer_address.bill_address_line = request_details[
                    "address_line"
                ]
                customer_address.bill_city = request_details["city"]
                customer_address.bill_region = request_details["region"]
                customer_address.bill_zip_code = request_details["zip"]
                customer_address.bill_country = (
                    request_details.get("country") or "Philippines"
                )
                customer_address.save()

                return render(
                    request,
                    "profile.html",
                    {
                        "customer": customer,
                        "customer_address": customer_address,
                    },
                )

        except CustomerAddress.DoesNotExist:
            customer = Customer.objects.get(customer_id=pk)
            customer_address = CustomerAddress(
                customer_id=customer,
                bill_address_line=request_details["address_line"],
                bill_city=request_details["city"],
                bill_region=request_details["region"],
                bill_zip_code=request_details["zip"],
                bill_country=request_details.get("country") or "Philippines",
            )
            customer_address.save()

            return render(
                request,
                "profile.html",
                {"customer": customer, "customer_address": customer_address},
            )


def add_product(request):
    if request.session.has_key("access"):
        if request.session["access"] == "admin" and request.session.has_key(
            "username"
        ):
            user = UserProfile.objects.get(
                username=request.session["username"]
            )
            admin = Administrator.objects.get(user_id=user)
            return render(
                request, "admin_products_add.html", {"profile": admin}
            )
    return render(request, "unauthorized.html")


def edit_product(request, variant_id):
    if variant_id:
        try:
            product = InventoryProduct.objects.get(variant_id=variant_id)
            return render(
                request, "admin_products_edit.html", {"product": product}
            )
        except InventoryProduct.DoesNotExist:
            return render(request, "unauthorized.html")


def admin_add_product(request):
    if request.method == "POST":
        request_details = request.POST

        if request.session.has_key("access"):
            if request.session[
                "access"
            ] == "admin" and request.session.has_key("username"):
                user = UserProfile.objects.get(
                    username=request.session["username"]
                )
                admin = Administrator.objects.get(user_id=user)
                product = InventoryProduct(
                    variant_name=request_details["variant_name"],
                    variant_sku=request_details["variant_sku"],
                    variant_description=request_details.get("variant_desc")
                    or "",
                    variant_stock=request_details["variant_stock"],
                    variant_price=request_details["variant_price"],
                    variant_image=request_details["variant_image"]
                    or DEFAULT_IMAGE,
                )
                product.save()

                return render(
                    request,
                    "admin_products.html",
                    {
                        "products": InventoryProduct.objects.filter(
                            variant_is_active=True
                        ),
                        "profile": admin,
                    },
                )
    return render(request, "unauthorized.html")


def admin_edit_product(request, variant_id):
    if request.method == "POST":
        request_details = request.POST

        if request.session.has_key("access"):
            if request.session[
                "access"
            ] == "admin" and request.session.has_key("username"):
                user = UserProfile.objects.get(
                    username=request.session["username"]
                )
                admin = Administrator.objects.get(user_id=user)
                product = InventoryProduct.objects.get(variant_id=variant_id)
                product.variant_price = request_details["variant_price"]
                product.variant_image = request_details["variant_image"]
                product.variant_description = request_details["variant_desc"]
                product.variant_name = request_details["variant_name"]
                product.variant_stock = request_details["variant_stock"]
                product.save()

                return render(
                    request,
                    "admin_products.html",
                    {
                        "products": InventoryProduct.objects.filter(
                            variant_is_active=True
                        ),
                        "profile": admin,
                    },
                )
    return render(request, "unauthorized.html")


def admin_delete_product(request, variant_id):
    if request.session.has_key("access"):
        if request.session["access"] == "admin" and request.session.has_key(
            "username"
        ):
            user = UserProfile.objects.get(
                username=request.session["username"]
            )
            admin = Administrator.objects.get(user_id=user)
            product = InventoryProduct.objects.get(variant_id=variant_id)
            product.variant_is_active = False
            product.save()

            return render(
                request,
                "admin_products.html",
                {
                    "products": InventoryProduct.objects.filter(
                        variant_is_active=True
                    ),
                    "profile": admin,
                },
            )
    return render(request, "unauthorized.html")


def admin_products(request):
    if request.session.has_key("access"):
        if request.session["access"] == "admin" and request.session.has_key(
            "username"
        ):
            user = UserProfile.objects.get(
                username=request.session["username"]
            )
            admin = Administrator.objects.get(user_id=user)
            return render(
                request,
                "admin_products.html",
                {
                    "products": InventoryProduct.objects.filter(
                        variant_is_active=True
                    ),
                    "profile": admin,
                },
            )
    return render(request, "unauthorized.html")


def admin_accounts(request):
    if request.session.has_key("access"):
        if request.session["access"] == "admin" and request.session.has_key(
            "username"
        ):
            user = UserProfile.objects.get(
                username=request.session["username"]
            )
            admin = Administrator.objects.get(user_id=user)
            return render(
                request,
                "admin_accounts.html",
                {"profile": admin, "admins": Administrator.objects.all()},
            )
    return render(request, "unauthorized.html")


def logout(request):
    if request.session.has_key("username"):
        del request.session["username"]
        request.session.modified = True

    return render(
        request,
        "index.html",
        {"products": InventoryProduct.objects.filter(variant_is_active=True)},
    )


def add_account(request):
    if request.session.has_key("access"):
        if request.session["access"] == "admin" and request.session.has_key(
            "username"
        ):
            user = UserProfile.objects.get(
                username=request.session["username"]
            )
            admin = Administrator.objects.get(user_id=user)
            return render(
                request, "admin_account_add.html", {"profile": admin}
            )
    return render(request, "unauthorized.html")


def admin_add_account(request):
    if request.session.has_key("access") and request.session.has_key(
        "username"
    ):
        if request.session["access"] != "admin":
            return render(request, "unauthorized.html")

    if request.method == "POST":
        post_request = request.POST
        password = post_request["password"]

        encoded_password = base64.b64encode(
            bytes(f"{password}-{password}".encode())
        ).decode()

        user_profile = UserProfile(
            username=post_request["username"],
            password=encoded_password,
            access_permissions="admin",
        )
        user_profile.save()

        admin_details = Administrator(
            first_name=post_request["first_name"],
            last_name=post_request["last_name"],
            position=post_request["position"],
            email=post_request["email"],
            user_id=user_profile,
        )
        admin_details.save()

        return render(
            request, "success.html", {"admin": request.session["username"]}
        )


def save_order(request, cust_id):
    request_details = request.POST

    if request.session.has_key("access") or request.session.has_key(
        "username"
    ):
        orders = {}
        for key, value in request_details.items():
            if "order-product" in key:
                orders.update({int(key[-1]): {"product": value, "qty": 0}})
            if "qty" in key:
                orders[int(key[-1])]["qty"] += int(value) if value else 0

        op_pks = []

        customer = Customer.objects.get(customer_id=cust_id)
        customer_address = CustomerAddress.objects.get(customer_id=customer)
        for key, value in orders.items():
            if not value["qty"]:
                continue
            product = InventoryProduct.objects.get(
                variant_sku=value["product"]
            )
            op = OrderedProduct(
                line_item_qty=value["qty"],
                line_item_price=product.variant_price,
                variant_name=product,
                customer_id=customer,
            )
            op_pks.append(op)
            op.save()

            product.variant_stock -= value["qty"]
            product.save()

        payment = Payment()
        payment.save()
        shipment = Shipment()
        shipment.save()

        total_qty = 0
        total_price = 0
        for op in op_pks:
            total_qty += op.line_item_qty
            total_price += op.line_item_price * op.line_item_qty

        total_tax_amount = total_price * 0.12
        so_trans_no = uuid.uuid4()
        so = SalesOrder(
            total_qty=total_qty,
            total_price=total_price,
            total_tax_amount=total_tax_amount,
            total_discount=0,
            total_order_amount=total_price + total_tax_amount,
            customer_address=customer_address,
            shipment_status=shipment,
            payment_status=payment,
            so_trans_no=so_trans_no,
            customer=customer,
        )
        so.save()

        payment.sales_order = so.so_trans_no
        shipment.sales_order = so.so_trans_no
        payment.save()
        shipment.save()

        for op in op_pks:
            op.sales_order_id = so
            op.save()

        automated_email_user = requests.post(
            "https://api.mailgun.net/v3/sandbox3348ea43eff3430fb8d285bf1bc299a4.mailgun.org/messages",
            auth=("api", "746e648aba12d0d558b4fef4696cb507-4d640632-fbb183ee"),
            data={
                "from": "Green Sunshine <ggreenssunshine@gmail.com>",
                "to": f"{customer.first_name} {customer.last_name} <{customer.email_address}>",
                "subject": f"Payment Details for {so.so_trans_no}",
                "text": f"Hello {customer.first_name},\n\n"
                f"Thank you for ordering with Green Sunshine! Please pay the exact amount and don't forget to fill up the payment form in the Orders page.\n\n"
                f"Total Amount: {so.total_order_amount}\n\n"
                f""
                f"PAYMAYA\t\tAdminFirstName AdminLastname\t09123456789\n"
                f"GCASH\t\tAdminFirstName AdminLastName\t09123456789\n"
                f"BPI\t\tAdminFirstName AdminLastName\t1231234560\n"
                f"UNIONBANK\tAdminFirstName AdminLastName\t1234567890\n\n"
                f"Regards,\n"
                f"AdminFirstName",
            },
        )

        orders_txt = ""
        for op in op_pks:
            orders_txt += f"\tProduct: {op.variant_name.variant_name}\t\tQty: {op.line_item_qty}\n"

        automated_email_admin = requests.post(
            "https://api.mailgun.net/v3/sandbox3348ea43eff3430fb8d285bf1bc299a4.mailgun.org/messages",
            auth=("api", "746e648aba12d0d558b4fef4696cb507-4d640632-fbb183ee"),
            data={
                "from": "Green Sunshine <ggreenssunshine@gmail.com>",
                "to": f"Green Sunshine <ggreenssunshine@gmail.com>",
                "subject": f"New Order - {so.so_trans_no}",
                "text": f"Customer: {customer.first_name} {customer.last_name}\n"
                f"Order No: {so.so_trans_no}\n"
                f"Orders:\n"
                f"{orders_txt}\n",
            },
        )

        if (
            automated_email_admin.status_code != 200
            or automated_email_user.status_code != 200
        ):
            return render(
                request,
                "success_order_email.html",
                {"trans_no": so_trans_no, "customer": customer},
            )

        return render(
            request,
            "success_order.html",
            {"trans_no": so_trans_no, "customer": customer},
        )
    return render(request, "unauthorized.html")


def admin_orders(request):
    if request.session.has_key("access"):
        if request.session["access"] == "admin" and request.session.has_key(
            "username"
        ):
            user = UserProfile.objects.get(
                username=request.session["username"]
            )
            admin = Administrator.objects.get(user_id=user)
            return render(
                request,
                "admin_orders.html",
                {"profile": admin, "sales_orders": SalesOrder.objects.all()},
            )
    return render(request, "unauthorized.html")


def admin_order_details(request, so_trans_no):
    if request.session.has_key("access"):
        if request.session["access"] == "admin":
            user = UserProfile.objects.get(
                username=request.session["username"]
            )
            admin = Administrator.objects.get(user_id=user)
            try:
                so = SalesOrder.objects.get(so_trans_no=so_trans_no)
                op = OrderedProduct.objects.filter(sales_order_id=so)
                payment = Payment.objects.get(
                    payment_id=so.payment_status.payment_id
                )
                shipment = Shipment.objects.get(
                    shipment_id=so.shipment_status.shipment_id
                )
                customer_address = CustomerAddress.objects.get(
                    cust_add_id=so.customer_address.cust_add_id
                )
                customer = Customer.objects.get(
                    customer_id=customer_address.customer_id.customer_id
                )

                return render(
                    request,
                    "admin_sales_order.html",
                    {
                        "profile": admin,
                        "so": so,
                        "op": op,
                        "payment_status": payment.payment_status.capitalize(),
                        "shipment_status": shipment.shipment_status.replace(
                            "_", " "
                        ).capitalize(),
                        "customer": customer,
                        "customer_address": customer_address,
                    },
                )
            except (
                SalesOrder.DoesNotExist,
                Administrator.DoesNotExist,
                OrderedProduct.DoesNotExist,
                Payment.DoesNotExist,
                Shipment.DoesNotExist,
                Customer.DoesNotExist,
                CustomerAddress.DoesNotExist,
            ):
                pass

    return render(request, "unauthorized.html")


def admin_payments(request):
    if request.session.has_key("access"):
        if request.session["access"] == "admin" and request.session.has_key(
            "username"
        ):
            user = UserProfile.objects.get(
                username=request.session["username"]
            )
            admin = Administrator.objects.get(user_id=user)
            return render(
                request,
                "admin_payments.html",
                {"profile": admin, "payments": Payment.objects.all()},
            )
    return render(request, "unauthorized.html")


def admin_shipments(request):
    if request.session.has_key("access"):
        if request.session["access"] == "admin" and request.session.has_key(
            "username"
        ):
            user = UserProfile.objects.get(
                username=request.session["username"]
            )
            admin = Administrator.objects.get(user_id=user)
            return render(
                request,
                "admin_shipments.html",
                {"profile": admin, "shipments": Shipment.objects.all()},
            )
    return render(request, "unauthorized.html")


def user_orders(request):
    if request.session.has_key("access"):
        if request.session["access"] == "user" and request.session.has_key(
            "username"
        ):
            user = UserProfile.objects.get(
                username=request.session["username"]
            )
            customer = Customer.objects.get(user_id=user)
            return render(
                request,
                "user_orders.html",
                {
                    "profile": customer,
                    "sales_orders": SalesOrder.objects.filter(
                        customer=customer
                    ),
                },
            )
    return render(request, "unauthorized.html")


def user_order_details(request, so_trans_no):
    if request.session.has_key("access"):
        if request.session["access"] == "user":
            user = UserProfile.objects.get(
                username=request.session["username"]
            )
            customer = Customer.objects.get(user_id=user)
            try:
                so = SalesOrder.objects.get(so_trans_no=so_trans_no)
                op = OrderedProduct.objects.filter(sales_order_id=so)
                payment = Payment.objects.get(
                    payment_id=so.payment_status.payment_id
                )
                shipment = Shipment.objects.get(
                    shipment_id=so.shipment_status.shipment_id
                )
                customer_address = CustomerAddress.objects.get(
                    cust_add_id=so.customer_address.cust_add_id
                )

                return render(
                    request,
                    "user_sales_order.html",
                    {
                        "profile": customer,
                        "so": so,
                        "op": op,
                        "payment_status": payment.payment_status.capitalize(),
                        "shipment_status": shipment.shipment_status.replace(
                            "_", " "
                        ).capitalize(),
                        "customer": customer,
                        "customer_address": customer_address,
                        "shipment": shipment,
                    },
                )
            except (
                SalesOrder.DoesNotExist,
                Administrator.DoesNotExist,
                OrderedProduct.DoesNotExist,
                Payment.DoesNotExist,
                Shipment.DoesNotExist,
                Customer.DoesNotExist,
                CustomerAddress.DoesNotExist,
            ):
                pass

    return render(request, "unauthorized.html")


def user_payment(request, so_trans_no):
    if request.session.has_key("username"):
        user = UserProfile.objects.get(username=request.session["username"])
        customer = Customer.objects.get(user_id=user)
        so = SalesOrder.objects.get(so_trans_no=so_trans_no)

        return render(
            request, "user_payment.html", {"profile": customer, "so": so}
        )
    return render(request, "unauthorized.html")


def user_paid(request, so_trans_no):
    if request.session.has_key("username"):
        user = UserProfile.objects.get(username=request.session["username"])
        customer = Customer.objects.get(user_id=user)
        so = SalesOrder.objects.get(so_trans_no=so_trans_no)
        payment = Payment.objects.get(sales_order=so_trans_no)
        shipment = Shipment.objects.get(sales_order=so_trans_no)

        if request.method == "POST":
            request_details = request.POST

            if so.total_order_amount != float(request_details["amount"]):
                print(so.total_order_amount, type(so.total_order_amount))
                print(
                    request_details["amount"], type(request_details["amount"])
                )
                return render(request, "unauthorized.html")

            payment.payment_date = request_details["payment_date"]
            payment.payment_method = request_details["payment_method"]
            payment.payment_trans_no = request_details["ref_num"]
            payment.payment_amount = request_details["amount"]
            payment.payment_status = "PAID"
            shipment.shipment_status = "Waiting for Confirmation"
            payment.save()
            shipment.save()

            requests.post(
                "https://api.mailgun.net/v3/sandbox3348ea43eff3430fb8d285bf1bc299a4.mailgun.org/messages",
                auth=(
                    "api",
                    "746e648aba12d0d558b4fef4696cb507-4d640632-fbb183ee",
                ),
                data={
                    "from": "Green Sunshine <ggreenssunshine@gmail.com>",
                    "to": f"Green Sunshine <ggreenssunshine@gmail.com>",
                    "subject": f"Order Paid - {so.so_trans_no}",
                    "text": f"Customer: {customer.first_name} {customer.last_name}\nTotal amount paid: Php {payment.payment_amount}\n",
                },
            )

        return render(
            request,
            "success_order.html",
            {"customer": customer, "trans_no": payment.payment_trans_no},
        )
    return render(request, "unauthorized.html")


def confirm_payment(request, so_trans_no):
    if request.session.has_key("username"):
        user = UserProfile.objects.get(username=request.session["username"])
        admin = Administrator.objects.get(user_id=user)
        shipment = Shipment.objects.get(sales_order=so_trans_no)

        shipment.shipment_status = "For Shipping"
        shipment.save()

        return render(request, "admin_dashboard.html", {"profile": admin})
    return render(request, "unauthorized.html")


def update_shipment(request, so_trans_no):
    if request.session.has_key("username"):
        if request.session["access"] == "admin":
            user = UserProfile.objects.get(
                username=request.session["username"]
            )
            admin = Administrator.objects.get(user_id=user)
            shipment = Shipment.objects.get(sales_order=so_trans_no)

            return render(
                request,
                "admin_shipment_edit.html",
                {"profile": admin, "shipment": shipment},
            )
    return render(request, "unauthorized.html")


def update_shipment_details(request, so_trans_no):
    if request.session.has_key("username"):
        user = UserProfile.objects.get(username=request.session["username"])
        so = SalesOrder.objects.get(so_trans_no=so_trans_no)
        customer = Customer.objects.get(customer_id=so.customer.customer_id)
        admin = Administrator.objects.get(user_id=user)
        shipment = Shipment.objects.get(sales_order=so_trans_no)

        if request.method == "POST":
            request_details = request.POST

            shipment.shipment_courier = request_details["courier"]
            shipment.shipment_id_url = request_details["track_num"]
            shipment.shipment_date = request_details["sdate"]
            shipment.shipment_status = "Shipped"
            shipment.save()

            requests.post(
                "https://api.mailgun.net/v3/sandbox3348ea43eff3430fb8d285bf1bc299a4.mailgun.org/messages",
                auth=(
                    "api",
                    "746e648aba12d0d558b4fef4696cb507-4d640632-fbb183ee",
                ),
                data={
                    "from": "Green Sunshine <ggreenssunshine@gmail.com>",
                    "to": f"{customer.first_name} {customer.last_name} <{customer.email_address}>",
                    "subject": f"Order Shipped - {so_trans_no}",
                    "text": f"Your order has been shipped!\n\n"
                    f"Courier: {shipment.shipment_courier}\n"
                    f"Tracking Number: {shipment.shipment_id_url}\n\n"
                    f"Thank you for trusting Green Sunshine!",
                },
            )

            return render(
                request,
                "admin_shipments.html",
                {"profile": admin, "shipments": Shipment.objects.all()},
            )
    return render(request, "unauthorized.html")


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox3348ea43eff3430fb8d285bf1bc299a4.mailgun.org/messages",
        auth=("api", "746e648aba12d0d558b4fef4696cb507-4d640632-fbb183ee"),
        data={
            "from": "Green Sunshine <ggreenssunshine@gmail.com>",
            "to": "Ma. Micah Encarnacion <emr2373@dlsud.edu.ph>",
            "subject": "Hello Ma. Micah Encarnacion",
            "text": "Congratulations Ma. Micah Encarnacion, you just sent an email with Mailgun!  You are truly awesome!",
        },
    )
