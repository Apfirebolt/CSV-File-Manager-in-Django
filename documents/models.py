from django.db import models
from csv_manager.settings import AUTH_USER_MODEL
import math


class UploadedFile(models.Model):
    uploaded_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='all_user_documents')
    uploaded_file = models.FileField(upload_to='csv_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_description = models.TextField()

    # Function to get the size of the uploaded CSV File
    def get_file_size(self):
        size_bytes = self.uploaded_file.size
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def __str__(self):
        return self.uploaded_by.username + ' - ' + self.file_description

    class Meta:
        verbose_name_plural = "User Documents"
