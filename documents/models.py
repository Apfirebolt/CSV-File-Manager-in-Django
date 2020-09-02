from django.db import models
from csv_manager.settings import AUTH_USER_MODEL


class UploadedFile(models.Model):
    uploaded_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='all_user_documents')
    uploaded_file = models.FileField(upload_to='csv_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_description = models.TextField()

    def __str__(self):
        return self.uploaded_by.username + ' - ' + self.file_description

    class Meta:
        verbose_name_plural = "User Documents"
