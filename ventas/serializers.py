from rest_framework import serializers
from .models import Venta, DetalleVenta
from productos.models import Producto
from decimal import Decimal
from django.db import transaction


class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    precio = serializers.DecimalField(source='producto.precio', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = DetalleVenta
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'precio', 'subtotal']
        read_only_fields = ['id', 'producto_nombre', 'precio', 'subtotal']


class VentaSerializer(serializers.ModelSerializer):
    # Para escritura (crear venta)
    detalles = DetalleVentaSerializer(many=True, required=False)
    
    # Para lectura (mostrar ventas con sus detalles)
    detalles_leidos = DetalleVentaSerializer(many=True, read_only=True, source='detalles')

    class Meta:
        model = Venta
        fields = ['id', 'fecha', 'total', 'detalles', 'detalles_leidos']

    def validate_detalles(self, value):
        if not value:
            raise serializers.ValidationError('La venta debe tener al menos un detalle')
        return value

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])

        with transaction.atomic():
            venta = Venta.objects.create(total=Decimal('0.00'))
            total = Decimal('0.00')

            for item in detalles_data:
                producto_id = item.get('producto')
                cantidad = Decimal(item.get('cantidad'))

                try:
                    producto = Producto.objects.select_for_update().get(pk=producto_id)
                except Producto.DoesNotExist:
                    raise serializers.ValidationError(f'Producto id={producto_id} no existe')

                if not producto.activo:
                    raise serializers.ValidationError(f'Producto "{producto.nombre}" está inactivo')

                if cantidad <= 0:
                    raise serializers.ValidationError(f'Cantidad inválida para "{producto.nombre}"')

                if cantidad > producto.stock:
                    raise serializers.ValidationError(f'Stock insuficiente para "{producto.nombre}". Disponible: {producto.stock}')

                precio_unitario = producto.precio
                if producto.precio_mayoreo and cantidad >= producto.cantidad_mayoreo:
                    precio_unitario = producto.precio_mayoreo

                subtotal = (Decimal(precio_unitario) * cantidad).quantize(Decimal('0.01'))

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    subtotal=subtotal
                )

                producto.stock = (Decimal(producto.stock) - cantidad).quantize(Decimal('0.01'))
                producto.save()

                total += subtotal

            venta.total = total.quantize(Decimal('0.01'))
            venta.save()

            return venta