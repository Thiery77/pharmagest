from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pharmacie.urls')),   # <-- C'est ce qui inclut les URLs de pharmacie
    path('accounts/', include('django.contrib.auth.urls')),
]