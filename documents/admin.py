from django.contrib import admin
from . models import UploadedFile


class CustomDocumentAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'file_description',)
    search_fields = ('file_description',)

admin.site.register(UploadedFile, CustomDocumentAdmin)

