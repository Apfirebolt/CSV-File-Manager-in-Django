from django import forms
from . models import UploadedFile
from django.core.validators import FileExtensionValidator


class CSVFileUploadForm(forms.ModelForm):
    error_messages = {
        'not_valid_csv': "The uploaded file is not in valid format. Please upload CSV files only.",
    }
    uploaded_file = forms.FileField(label=("Please Upload Your CSV File."),
                                    widget=forms.FileInput(attrs={'class': 'form-control-file'}),
                                    validators=[FileExtensionValidator(['csv', ])])
    file_description = forms.CharField(label=("Please Enter File Description"),
                                widget=forms.Textarea(attrs={'class': 'form-control'}),)

    class Meta:
        model = UploadedFile
        fields = ('uploaded_file', 'file_description',)



