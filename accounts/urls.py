from django.urls import path
from django.conf.urls.static import static
from csv_manager import settings
from . views import CreateUserView, DeleteAccountView, DetailUserView, LogoutView, login_user


urlpatterns = [
    path('', DetailUserView.as_view(template_name='accounts/dashboard.html'), name='dashboard'),
    path('register', CreateUserView.as_view(), name='register'),
    path('login', login_user, name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('delete', DeleteAccountView, name='delete_account'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
