from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from .serializers import LoginSerializer, ChangePasswordSerializer, UsuarioSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            try:
                usuario = Usuario.objects.get(username=username)
                if usuario.check_password(password):
                    return Response({
                        'success': True,
                        'user': UsuarioSerializer(usuario).data
                    })
                else:
                    return Response({'success': False, 'error': 'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)
            except Usuario.DoesNotExist:
                return Response({'success': False, 'error': 'Usuario no encontrado'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'success': False, 'error': 'Datos inválidos'}, status=status.HTTP_400_BAD_REQUEST)


class ChangeCredentialsView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_username = serializer.validated_data['new_username']
            new_password = serializer.validated_data['new_password']
            
            try:
                usuario = Usuario.objects.get(es_admin=True)
                usuario.username = new_username
                usuario.set_password(new_password)
                usuario.save()
                return Response({'success': True, 'message': 'Credenciales actualizadas'})
            except Usuario.DoesNotExist:
                usuario = Usuario(username=new_username, es_admin=True)
                usuario.set_password(new_password)
                usuario.save()
                return Response({'success': True, 'message': 'Credenciales creadas'})
        return Response({'success': False, 'error': 'Datos inválidos'}, status=status.HTTP_400_BAD_REQUEST)


class VerificarUsuarioView(APIView):
    def get(self, request):
        try:
            usuario = Usuario.objects.get(es_admin=True)
            return Response({'exists': True, 'username': usuario.username})
        except Usuario.DoesNotExist:
            return Response({'exists': False})