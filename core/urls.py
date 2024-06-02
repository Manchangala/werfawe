from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('producto/<int:producto_id>/crear_pedido/', views.crear_pedido, name='crear_pedido'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('pedido/<int:pedido_id>/proceso/', views.proceso_pedido, name='proceso_pedido'), 
   
]

