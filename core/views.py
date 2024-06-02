from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Producto, Pedido
from .forms import RegistroForm, LoginForm, SeleccionProductoForm, ConfirmacionPersonalizacionForm, MetodoEntregaForm, PagoForm

def home(request):
    return render(request, 'core/home.html')

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'core/lista_productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'core/detalle_producto.html', {'producto': producto})

@login_required
def crear_pedido(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    pedido = Pedido.objects.create(cliente=request.user, producto=producto, cantidad=1, direccion_entrega='Dirección de prueba', fecha_entrega='2024-06-01')
    return redirect('proceso_pedido', pedido_id=pedido.id)

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def pedido_exitoso(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'core/pedido_exitoso.html', {'pedido': pedido})

@login_required
def proceso_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    step = int(request.GET.get('step', 1))

    if step == 1:
        if request.method == 'POST':
            form = SeleccionProductoForm(request.POST)
            if form.is_valid():
                # Procesar selección de producto
                step = 2
                return redirect('proceso_pedido', pedido_id=pedido.id, step=step)
        else:
            form = SeleccionProductoForm()
    elif step == 2:
        if request.method == 'POST':
            form = ConfirmacionPersonalizacionForm(request.POST)
            if form.is_valid():
                # Procesar confirmación y personalización del pedido
                step = 3
                return redirect('proceso_pedido', pedido_id=pedido.id, step=step)
        else:
            form = ConfirmacionPersonalizacionForm()
    elif step == 3:
        if request.method == 'POST':
            form = MetodoEntregaForm(request.POST)
            if form.is_valid():
                # Procesar elección de método de entrega
                step = 4
                return redirect('proceso_pedido', pedido_id=pedido.id, step=step)
        else:
            form = MetodoEntregaForm()
    elif step == 4:
        if request.method == 'POST':
            form = PagoForm(request.POST)
            if form.is_valid():
                # Procesar pago y finalizar pedido
                pedido.estado = 'completado'
                pedido.save()
                return redirect('pedido_exitoso', pedido_id=pedido.id)
        else:
            form = PagoForm()
    else:
        form = None

    return render(request, 'core/proceso_pedido.html', {'pedido': pedido, 'step': step, 'form': form})
