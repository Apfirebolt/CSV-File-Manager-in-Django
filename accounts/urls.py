from django.urls import path
from django.conf.urls.static import static
from csv_manager import settings
from . views import CreateUserView, DeleteAccountView, DetailUserView, LogoutView, login_user
from documents.views import ( UploadNewFile, DeleteUploadedFile, DetailUploadedFile,
    ListUploadedFiles, UpdateUploadedFile, )


urlpatterns = [
    path('', DetailUserView.as_view(template_name='accounts/dashboard.html'), name='dashboard'),
    path('register', CreateUserView.as_view(), name='register'),
    path('login', login_user, name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('delete', DeleteAccountView.as_view(), name='delete_account'),
    path('all_files', ListUploadedFiles.as_view(), name='all_files'),
    path('file_upload', UploadNewFile.as_view(), name='upload_file'),
    path('file_update/<int:id>', UpdateUploadedFile.as_view(), name='update_file'),
    path('file_detail/<int:id>', DetailUploadedFile.as_view(), name='detail_file'),
    path('file_delete/<int:id>', DeleteUploadedFile.as_view(), name='delete_file'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
