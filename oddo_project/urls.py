from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Apps antiguas (compatibilidad)
    path('api/', include('api.urls')),
    # Nuevas apps modulares
    path('api/', include('core.urls')),         # Partners y Products
    path('api/', include('purchases.urls')),    # Purchase Orders
    path('api/', include('inventory.urls')),    # Warehouses y Stock
    path('api/', include('pos.urls')),          # POS Orders
    path('api/', include('invoicing.urls')),    # Invoices y Payments
    path('api/', include('hr.urls')),           # Employees
    # Mesas - Vista gráfica y API
    path('mesas/', include('mesas.urls')),      # Interfaz gráfica de mesas
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
