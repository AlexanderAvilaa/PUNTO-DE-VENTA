from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    codigo_barras = models.CharField(max_length=100, unique=True, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_mayoreo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cantidad_mayoreo = models.PositiveIntegerField(default=1)
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Decimal para soportar kg
    es_granel = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.codigo_barras}"