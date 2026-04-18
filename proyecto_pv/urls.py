from django.urls import path, include
from rest_framework.routers import DefaultRouter
from productos.views import ProductoViewSet
from ventas.views import VentaViewSet
from auth_app.views import LoginView, ChangeCredentialsView, VerificarUsuarioView

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'ventas', VentaViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/change-credentials/', ChangeCredentialsView.as_view(), name='change-credentials'),
    path('api/verificar-usuario/', VerificarUsuarioView.as_view(), name='verificar-usuario'),
]