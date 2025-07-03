from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('dashboard')),  # ← aquí está el cambio
    path('admin/', admin.site.urls),
    path('empresa/', include('empresa.urls')),
]
