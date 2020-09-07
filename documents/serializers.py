from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import UploadedFile
import pandas as pd
from pandas.api.types import is_numeric_dtype


class UploadedFileSerializer(serializers.ModelSerializer):

  uploaded_file = serializers.FileField(required=False)
  file_description = serializers.CharField(max_length=300)

  class Meta:
    model = UploadedFile
    fields = ('uploaded_by', 'uploaded_file', 'file_description',)
    read_only_fields = ['uploaded_by']

  def validate_uploaded_file(self, value):
    df = pd.read_csv(value.file)
    # Check uniqueness of the id column
    if not df['id'].is_unique:
      raise ValidationError("ID column of the uploaded CSV file is not unique.")
    # Check integer data type of sessions column
    if not is_numeric_dtype(df['sessions']):
      raise ValidationError("Sessions column data is not int type.")
    # Check integer data type of sessions column
    if not is_numeric_dtype(df['page_views']):
      raise ValidationError("Page column data is not of int type.")
    # Check if sessions is greater than pages in any entry
    new_df = df[df['page_views'] < df['sessions']]
    if not new_df.empty:
      raise ValidationError("One or more rows have session value more than page value.")
    return value


class ViewDocumentSerializer(serializers.ModelSerializer):

  class Meta:
    model = UploadedFile
    fields = ('id', 'uploaded_file', 'file_description', 'uploaded_at',)
