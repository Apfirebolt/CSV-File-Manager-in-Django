from django import forms
from . models import UploadedFile
from django.core.validators import FileExtensionValidator
import pandas as pd


class CSVFileUploadForm(forms.ModelForm):
    error_messages = {
        'not_valid_csv': "The uploaded file is not in valid format. Please upload CSV files only.",
        'session_less_than_page': "Sessions Views should always be less than page views."
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
        # try:
        #     df = pd.read_csv(uploaded_file.file, nrows=5)
        #     for index, row in df.iterrows():
        #         print(row)
        #     for name, dtype in df.dtypes.iteritems():
        #         print(name, dtype)
        # except Exception as err:
        #     print(err)
        return uploaded_file



