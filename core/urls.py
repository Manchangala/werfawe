from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('confirmacion_pedido/', views.confirmacion_pedido, name='confirmacion_pedido'),
    path('eleccion_entrega/', views.eleccion_entrega, name='eleccion_entrega'),
    path('pago_finalizacion/', views.pago_finalizacion, name='pago_finalizacion'),
    path('pedido_exitoso/<int:pedido_id>/', views.pedido_exitoso, name='pedido_exitoso'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),  # Asegúrate de que esta línea exista
    path('producto/<int:producto_id>/crear_pedido/', views.crear_pedido, name='crear_pedido'),
]

