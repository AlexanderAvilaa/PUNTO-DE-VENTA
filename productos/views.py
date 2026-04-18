from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        codigo_barras = self.request.query_params.get('codigo_barras', None)
        
        if codigo_barras is not None:
            # Filtro EXACTO
            queryset = queryset.filter(codigo_barras=codigo_barras)
        
        return queryset