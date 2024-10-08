"""
URL configuration for rice_harvest_schedule project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# from auth_admin.admin import admin_site  # Import the custom admin site
from drivers.views import *
urlpatterns = [
    path('admin/', admin.site.urls),  # Use the custom admin site
    # path("accounts/", include("allauth.urls")),
    path('', include('accounts.urls')),
    path('drivers/', include('drivers.urls')),
    path('bookings/', include('bookings.urls')),
    path('authadmin/', include('auth_admin.urls')),
    path('oauth2callback/', oauth2callback, name='oauth2callback'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

