from django.urls import path
from django.conf.urls.static import static
from csv_manager import settings
from . views import ( CreateUserView, DeleteAccountView, DetailUserView, LogoutView, login_user,
                    RegisterUserApiView, CustomObtainAuthToken, ListAllUsersApiView, )
from documents.views import ( UploadNewFile, DeleteUploadedFile, DetailUploadedFile,
                            ListUploadedFiles, UpdateUploadedFile, GetAllDocumentsAPI,
                              GetDocumentDetail, UploadFileAPIView, UpdateFileAPIView, DeleteFileAPIView, )


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
    # API Urls start from here
    path('api/register', RegisterUserApiView.as_view(), name='register_api'),
    path('api/auth-token', CustomObtainAuthToken.as_view(), name='auth-token'),
    path('api/users', ListAllUsersApiView.as_view(), name='users_api'),
    path('api/documents', GetAllDocumentsAPI.as_view(), name='all_documents_api'),
    path('api/file_upload', UploadFileAPIView.as_view(), name='upload_file_api'),
    path('api/delete_file/<int:id>', DeleteFileAPIView.as_view(), name='delete_file_api'),
    path('api/update_file/<int:id>', UpdateFileAPIView.as_view(), name='update_file_api'),
    path('api/<int:pk>', GetDocumentDetail.as_view(), name='document_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
