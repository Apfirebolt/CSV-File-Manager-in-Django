from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from csv_manager import settings
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='homepage.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
]

handler404 = views.handler404
handler403 = views.handler403
handler400 = views.handler400

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
