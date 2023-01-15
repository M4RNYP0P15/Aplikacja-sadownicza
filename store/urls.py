from django.contrib import admin
from django.urls import path
from .views.home import Index, store
# from .views.signup import Signup
from .views.signup import customer_signup_view
# from .views.login import Login, logout, afterlogin_view
from .views.login import afterlogin_view, custom_login, custom_logout
from .views.cart import cart_view
from .views.checkout import CheckOut
from .views.orders import my_order_view
from .views.password_back import password_change, password_reset_request, passwordResetConfirm, activate
# from .middleware.auth import auth_middleware
# from django.contrib.auth.views import LogoutView, LoginView
from .views.profile import profile
from .views.admin_dashboard import admin_dashboard_view, admin_add_product_view, admin_products_view, admin_view_booking_view, view_customer_view, delete_order_view, update_order_view, delete_product_view, update_product_view, delete_customer_view, update_customer_view
app_name = "store"

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store, name='store'),


    # path('signup', Signup.as_view(), name='signup'),
    path('signup', customer_signup_view),
    # path('login', LoginView.as_view(template_name='login.html'),name='login'),
    path('login', custom_login, name='login'),
    path('logged', afterlogin_view, name='afterlogin'),
    # path('logout', LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('logout', custom_logout, name='logout'),
    path('profile/<username>', profile, name='profile'),

    path("password_change", password_change, name="password_change"),
    path("password_reset", password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', passwordResetConfirm, name='password_reset_confirm'),

    path("activate/<uidb64>/<token>", activate, name='activate'),
    # path('customer-home', views.customer_home_view,name='customer-home'),

    path('admin-dashboard', admin_dashboard_view,name='admin-dashboard'),
    path('view-customer', view_customer_view,name='view-customer'),
    path('delete-customer/<int:pk>', delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', update_customer_view,name='update-customer'),

    path('admin-products', admin_products_view,name='admin-products'),
    path('admin-add-product', admin_add_product_view,name='admin-add-product'),
    path('delete-product/<int:pk>', delete_product_view,name='delete-product'),
    path('update-product/<int:pk>', update_product_view,name='update-product'),

    path('admin-view-booking', admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', update_order_view,name='update-order'),
    
    # path('cart', auth_middleware(Cart.as_view()), name='cart'),
    path('cart', cart_view, name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('orders', my_order_view, name='orders'),
]