from django import forms
from . models import UploadedFile
from django.core.validators import FileExtensionValidator
import pandas as pd
from pandas.api.types import is_numeric_dtype


class CSVFileUploadForm(forms.ModelForm):
    error_messages = {
        'not_valid_csv': "The uploaded file is not in valid format. Please upload CSV files only.",
        'session_more_than_page': "Sessions Views should always be less than page views.",
        'id_not_unique': "ID column of the CSV file uploaded should be unique.",
        'session_not_numeric': "Values in session column should be numeric type.",
        'page_not_numeric': "Values in page column should be numeric type."
    }
    uploaded_file = forms.FileField(label=("Please Upload Your CSV File."),
                                    widget=forms.FileInput(attrs={'class': 'form-control-file'}),
                                    validators=[FileExtensionValidator(['csv', ])])
    file_description = forms.CharField(label=("Please Enter File Description"),
                                widget=forms.Textarea(attrs={'class': 'form-control'}),)

    class Meta:
        model = UploadedFile
        fields = ('uploaded_file', 'file_description',)

    def clean_uploaded_file(self):
        uploaded_file = self.cleaned_data.get('uploaded_file')
        df = pd.read_csv(uploaded_file.file)
        # Check if sessions is greater than pages in any entry
        new_df = df[df['page_views'] < df['sessions']]
        if not new_df.empty:
            raise forms.ValidationError(
                self.error_messages['session_more_than_page'],
                code='session_more_than_page'
            )
        # Check uniqueness of the id column
        if not df['id'].is_unique:
            raise forms.ValidationError(
                self.error_messages['id_not_unique'],
                code='id_not_unique'
            )
        # Check integer data type of sessions column
        if not is_numeric_dtype(df['sessions']):
            raise forms.ValidationError(
                self.error_messages['session_not_numeric'],
                code='session_not_numeric'
            )
        # Check integer data type of sessions column
        if not is_numeric_dtype(df['page_views']):
            raise forms.ValidationError(
                self.error_messages['page_not_numeric'],
                code='page_not_numeric'
            )
        return uploaded_file



