"""aiprojects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework.reverse import reverse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.conf.urls.static import static


def system_health_check(request):
    return JsonResponse({
        "success": True,
        "health_check": "pass",
        "message": f"Check the swagger UI {reverse('schema-swagger-ui', request=request)}",
    })


schema_view = get_schema_view(
    openapi.Info(
        title="AI Projects API",
        default_version='v1',
        description="Chamara Herath",
        contact=openapi.Contact(email="developer@chamara.cc"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('facenet/', include('facenet.urls')),
    path('', system_health_check, name="system_health_check"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Text to put at the end of each page's <title>.
admin.site.site_title = 'AI Projects - Chamara'

# Text to put in each page's <h1>.
admin.site.site_header = 'AI Project - Admin'

# Text to put at the top of the admin index page.
admin.site.index_title = 'Site administration'
