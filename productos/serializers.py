from rest_framework import serializers
from .models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

    def validate_precio(self, value):
        if value < 0:
            raise serializers.ValidationError('El precio debe ser mayor o igual a 0')
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('El stock debe ser mayor o igual a 0')
        return value

    def validate_cantidad_mayoreo(self, value):
        if value < 1:
            raise serializers.ValidationError('La cantidad para mayoreo debe ser al menos 1')
        return value

    def validate(self, attrs):
        precio_mayoreo = attrs.get('precio_mayoreo')
        precio = attrs.get('precio')
        if precio_mayoreo is not None and precio is not None:
            try:
                if precio_mayoreo > precio:
                    raise serializers.ValidationError('El precio de mayoreo no puede ser mayor que el precio normal')
            except TypeError:
                pass
        return attrs