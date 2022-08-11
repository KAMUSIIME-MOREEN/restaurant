
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home_page, name="homepage"),
    path('login/', views.login_page, name="loginpage"),
     path('logout/', views.logout_page, name="logoutpage"),
    path('registration/', views.reg_page, name="regpage"),
    path('orders/', views.orders_page, name="orderspage"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)