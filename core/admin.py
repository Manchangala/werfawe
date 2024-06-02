from django.contrib import admin
from .models import Categoria, Producto, Cliente

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'direccion', 'telefono')

admin.site.register(Cliente, ClienteAdmin)


admin.site.register(Categoria)
admin.site.register(Producto)

