"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
# Use include() to add paths from the catalog application
from django.urls import include
from django.views.generic import RedirectView
from django.urls import path
# Use static() to add url mapping to serve
# static files during development (only)
from django.conf import settings
from django.conf.urls.static import static
from feedback.views import FeedbackView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('feedback/', FeedbackView.as_view(), name="feedback"),
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    # Add URL maps to redirect the base URL to our application
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serving static files during development
# eg if your STATIC_URL is defined as /static/,
# you can add the above snippet

# You don't need to run staticfiles when you're
# running a development server and DEBUG is set to True.

# Static and media files can be then served directly via the web process
