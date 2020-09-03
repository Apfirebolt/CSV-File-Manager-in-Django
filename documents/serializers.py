from rest_framework import serializers
from .models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):

  class Meta:
    model = UploadedFile
    fields = ('uploaded_by', 'uploaded_file', 'file_description',)
    read_only_fields = ['uploaded_by']


class ViewDocumentSerializer(serializers.ModelSerializer):

  class Meta:
    model = UploadedFile
    fields = ('id', 'uploaded_file', 'file_description',)
