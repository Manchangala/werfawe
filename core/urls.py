from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static
from core.views import PedidoWizard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('producto/<int:producto_id>/crear_pedido/', views.crear_pedido, name='crear_pedido'),
    path('pedido/<int:pedido_id>/proceso/', views.proceso_pedido, name='proceso_pedido'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pedido_exitoso/<int:pedido_id>/', views.pedido_exitoso, name='pedido_exitoso'),
    path('pedido_wizard/', PedidoWizard.as_view(), name='pedido_wizard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


