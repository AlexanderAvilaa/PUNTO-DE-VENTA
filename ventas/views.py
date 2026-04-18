from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Venta, DetalleVenta
from .serializers import VentaSerializer, DetalleVentaSerializer
from productos.models import Producto
from decimal import Decimal

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by('-fecha')
    serializer_class = VentaSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        detalles_data = data.get('detalles', [])
        
        if not detalles_data:
            return Response({'error': 'La venta debe tener al menos un detalle'}, status=400)
        
        # Crear la venta
        venta = Venta.objects.create(total=0)
        total_venta = Decimal('0.00')
        
        for item in detalles_data:
            producto_id = item.get('producto')
            cantidad = Decimal(str(item.get('cantidad')))
            
            try:
                producto = Producto.objects.get(id=producto_id)
            except Producto.DoesNotExist:
                return Response({'error': f'Producto {producto_id} no existe'}, status=400)
            
            # Verificar stock
            if cantidad > producto.stock:
                return Response({'error': f'Stock insuficiente para {producto.nombre}'}, status=400)
            
            # Calcular subtotal
            subtotal = producto.precio * cantidad
            total_venta += subtotal
            
            # Crear detalle
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                subtotal=subtotal
            )
            
            # Actualizar stock
            producto.stock -= cantidad
            producto.save()
        
        # Actualizar total de la venta
        venta.total = total_venta
        venta.save()
        
        serializer = self.get_serializer(venta)
        return Response(serializer.data, status=201)
    
    @action(detail=True, methods=['get'])
    def detalles(self, request, pk=None):
        venta = self.get_object()
        detalles = venta.detalleventa_set.all()
        serializer = DetalleVentaSerializer(detalles, many=True)
        return Response(serializer.data)