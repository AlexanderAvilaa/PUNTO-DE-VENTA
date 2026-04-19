Backend & Frontend
Bienvenido al sistema de Punto de Venta. Este proyecto está diseñado con una arquitectura moderna de desacoplamiento, 
utilizando Django como un motor de API robusto y React para una interfaz de usuario ágil y reactiva.

===============================================================
Arquitectura del Proyecto
El sistema se divide en dos pilares principales:

Backend (Cerebro): Django + Django REST Framework. Gestiona la lógica de negocio, autenticación y base de datos (SQLite por defecto).

Frontend (Interfaz): React potenciado por Vite. Una SPA (Single Page Application) que consume la API de forma asíncrona.

================================================================
Requisitos Previos
Antes de empezar, asegúrate de tener instalado:

* Python 3.10+
* Node.js 18 LTS+ (con npm)
* SQLite3 (integrado en el proyecto)

=================================================================
Guía de Instalación Paso a Paso
1. Preparar el Backend
Navega al corazón del sistema y configura el entorno:

cd backend
# Activa tu entorno (Windows)
.\entorno\Scripts\Activate.ps1  # PowerShell
.\entorno\Scripts\activate.bat  # CMD

# Instalar dependencias
pip install -r requirements.txt || pip install django djangorestframework django-cors-headers

Inicialización de datos:
Ejecuta las migraciones y crea al administrador maestro:
python manage.py migrate
python manage.py crear_admin  # Genera usuario 'admin' / contraseña '1234'
python manage.py runserver

    El servidor estará vivo en: http://127.0.0.1:8000

2. Preparar el Frontend
Abre una nueva terminal y levanta la interfaz visual:

cd frontend
npm install
npm run dev

  Accede a la aplicación en: http://localhost:5173

Exploración de la API (Endpoints)
La comunicación se realiza a través de http://127.0.0.1:8000/api/. Aquí los puntos clave:
Gestión de Inventario (/productos/)
Listar/Crear: GET / POST.

Detalle/Acciones: GET / PUT / DELETE mediante el id.

Lógica de Negocio: El sistema valida automáticamente que el stock y precios sean coherentes.

Procesamiento de Ventas (/ventas/)
Registrar Venta: Envía un JSON con los IDs de productos y cantidades.

Regla de Oro: El sistema aplica automáticamente el precio de mayoreo si la cantidad alcanza el umbral definido en el producto. Además, descuenta el stock en tiempo real.

🔐 Seguridad y Acceso
Login: /api/login/ para autenticación.

Gestión: /api/change-credentials/ para actualizar el acceso del administrador.

Configuración y Variables de Entorno
Para pasar a un entorno profesional, copia el archivo .env.example a uno nuevo llamado .env.

| Variable | Propósito | 
| :----------- | :----------: | 
| SECRET_KEY | Llave maestra de seguridad de Django.    |
| DEBUG     | True para desarrollo, False para producción.     | 
| DB_...   | Configuración para PostgreSQL (opcional). |

Documentación Interactiva (Swagger)
¿Quieres probar la API sin usar Postman? Hemos integrado Swagger.

Instala: pip install drf-spectacular
Configura settings.py y urls.py (ver sección de documentación técnica).
Visita: http://127.0.0.1:8000/api/docs/ para interactuar con todos los endpoints de forma visual.

