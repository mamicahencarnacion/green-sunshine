"""
    Created by Ma. Micah Encarnacion on 12/08/2020
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("register-user", views.register_new_user, name="register-user"),
    path("login-user", views.login_user, name="login-user"),
    path("add-products", views.add_product, name="add-products"),
    path(
        "delete-product/<int:variant_id>",
        views.admin_delete_product,
        name="delete-product",
    ),
    path(
        "edit-shipping-address/<int:pk>",
        views.shipping,
        name="edit-shipping-address",
    ),
    path(
        "update-shipping-address/<int:pk>",
        views.update_shipping,
        name="update-shipping-address",
    ),
    path(
        "edit-billing-address/<int:pk>",
        views.billing,
        name="edit-billing-address",
    ),
    path(
        "update-billing-address/<int:pk>",
        views.update_billing,
        name="update-billing-address",
    ),
    path("admin/products", views.admin_products, name="admin-products"),
    path("admin/accounts", views.admin_accounts, name="admin-accounts"),
    path("add-administrator", views.add_account, name="add-administrator"),
    path(
        "admin/products/add",
        views.admin_add_product,
        name="admin-products-add",
    ),
    path(
        "admin/products/edit/<int:variant_id>",
        views.admin_edit_product,
        name="admin-products-edit",
    ),
    path(
        "product-details/<int:pk>",
        views.product_details,
        name="product-details",
    ),
    path("logout", views.logout, name="logout"),
    path("order", views.order_form, name="order_form"),
    path("submit-order/<int:cust_id>", views.save_order, name="save_order"),
    path(
        "edit-products/<int:variant_id>",
        views.edit_product,
        name="edit-products",
    ),
    path(
        "admin/accounts/add", views.admin_add_account, name="admin-account-add"
    ),
    path("admin/orders", views.admin_orders, name="admin-orders"),
    path(
        "admin/orders/<str:so_trans_no>",
        views.admin_order_details,
        name="admin-order",
    ),
    path("admin/payments", views.admin_payments, name="admin-payments"),
    path("admin/shipments", views.admin_shipments, name="admin-shipments"),
    path("user/orders", views.user_orders, name="user-orders"),
    path(
        "user/orders/<str:so_trans_no>",
        views.user_order_details,
        name="user-order",
    ),
    path(
        "user/orders/<str:so_trans_no>/payment",
        views.user_payment,
        name="user-payment",
    ),
    path("user/payment/<str:so_trans_no>", views.user_paid, name="user-paid"),
    path(
        "admin/payment/confirm/<str:so_trans_no>",
        views.confirm_payment,
        name="confirm-payment",
    ),
    path(
        "admin/shipment/update/<str:so_trans_no>",
        views.update_shipment,
        name="update-shipment",
    ),
    path(
        "admin/shipment/<str:so_trans_no>",
        views.update_shipment_details,
        name="update-shipment-details",
    ),
]
