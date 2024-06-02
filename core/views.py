
from django.shortcuts import render, get_object_or_404
from .models import Producto
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.shortcuts import render, get_object_or_404
from .models import Producto
from django.shortcuts import render, redirect
from .models import Pedido, Producto, PedidoProducto,Cliente
from .forms import PedidoForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente


def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'core/lista_productos.html', {'productos': productos})



def home(request):
    return render(request, 'core/home.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            direccion = request.POST.get('direccion')
            telefono = request.POST.get('telefono')
            Cliente.objects.create(usuario=user, direccion=direccion, telefono=telefono)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_productos')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'core/detalle_producto.html', {'producto': producto})


def crear_pedido(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.cliente = request.user.cliente
            pedido.producto = producto
            pedido.save()
            return redirect('proceso_pedido', pedido_id=pedido.id)  # Redirigir a proceso_pedido con pedido_id
    else:
        form = PedidoForm()
    return render(request, 'core/crear_pedido.html', {'form': form, 'producto': producto})


def seleccion_producto(request):
    productos = Producto.objects.all()
    if request.method == 'POST':
        productos_seleccionados = request.POST.getlist('productos')
        cantidades = {producto_id: request.POST[f'cantidad_{producto_id}'] for producto_id in productos_seleccionados}
        request.session['productos_seleccionados'] = productos_seleccionados
        request.session['cantidades'] = cantidades
        return redirect('confirmacion_pedido')
    return render(request, 'core/seleccion_producto.html', {'productos': productos})


def confirmacion_pedido(request):
    productos_seleccionados = request.session.get('productos_seleccionados', [])
    cantidades = request.session.get('cantidades', {})
    productos = Producto.objects.filter(id__in=productos_seleccionados)
    if request.method == 'POST':
        peticiones_especiales = request.POST.get('peticiones_especiales', '')
        request.session['peticiones_especiales'] = peticiones_especiales
        return redirect('eleccion_entrega')
    return render(request, 'core/confirmacion_pedido.html', {'productos': productos, 'cantidades': cantidades})

def eleccion_entrega(request):
    if request.method == 'POST':
        tipo_entrega = request.POST.get('tipo_entrega')
        direccion_entrega = request.POST.get('direccion_entrega')
        fecha_entrega = request.POST.get('fecha_entrega')
        request.session['tipo_entrega'] = tipo_entrega
        request.session['direccion_entrega'] = direccion_entrega
        request.session['fecha_entrega'] = fecha_entrega
        return redirect('pago_finalizacion')
    return render(request, 'core/eleccion_entrega.html')


def pago_finalizacion(request):
    if request.method == 'POST':
        cliente, created = Cliente.objects.get_or_create(usuario=request.user, defaults={
            'direccion': 'Dirección por defecto',
            'telefono': '0000000000'
        })
        productos_seleccionados = request.session.get('productos_seleccionados', [])
        cantidades = request.session.get('cantidades', {})
        tipo_entrega = request.session.get('tipo_entrega')
        direccion_entrega = request.session.get('direccion_entrega')
        fecha_entrega = request.session.get('fecha_entrega')
        peticiones_especiales = request.session.get('peticiones_especiales', '')
        pedido = Pedido.objects.create(
            cliente=cliente,
            direccion_entrega=direccion_entrega,
            fecha_entrega=fecha_entrega,
            estado='pendiente'
        )
        for producto_id in productos_seleccionados:
            cantidad = cantidades.get(producto_id, 1)
            producto = Producto.objects.get(id=producto_id)
            PedidoProducto.objects.create(pedido=pedido, producto=producto, cantidad=cantidad)
        return redirect('pedido_exitoso', pedido_id=pedido.id)
    return render(request, 'core/pago_finalizacion.html')

def pedido_exitoso(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'core/pedido_exitoso.html', {'pedido': pedido})


def proceso_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    step = request.GET.get('step', 1)
    step = int(step)
    if step == 1:
        if request.method == 'POST':
            # Manejar selección de producto
            step = 2
            return redirect('proceso_pedido', pedido_id=pedido.id, step=step)
    elif step == 2:
        if request.method == 'POST':
            # Manejar confirmación y personalización del pedido
            step = 3
            return redirect('proceso_pedido', pedido_id=pedido.id, step=step)
    elif step == 3:
        if request.method == 'POST':
            # Manejar elección de método de entrega
            step = 4
            return redirect('proceso_pedido', pedido_id=pedido.id, step=step)
    elif step == 4:
        if request.method == 'POST':
            # Manejar pago y finalización del pedido
            pedido.estado = 'completado'
            pedido.save()
            return redirect('pedido_exitoso', pedido_id=pedido.id)
    return render(request, 'core/proceso_pedido.html', {'pedido': pedido, 'step': step})