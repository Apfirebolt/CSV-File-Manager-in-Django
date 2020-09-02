from django.views.generic import FormView, ListView, UpdateView, DeleteView, DetailView
from . forms import CSVFileUploadForm
from . models import UploadedFile
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import reverse


class UploadNewFile(LoginRequiredMixin, FormView):
    """ This class would upload a new file using form """
    template_name = 'documents/upload_file.html'
    form_class = CSVFileUploadForm

    def form_valid(self, form):
        # create new user instance and save data
        new_document_obj = UploadedFile()
        new_document_obj.file_description = form.cleaned_data['file_description']
        new_document_obj.uploaded_file = form.cleaned_data['uploaded_file']
        new_document_obj.uploaded_by = self.request.user
        new_document_obj.save()
        messages.add_message(self.request, messages.INFO, 'You have successfully uploaded a file!')
        return HttpResponseRedirect(reverse('accounts:all_files'))

    def form_invalid(self, form):
        # If form is invalid return superclass method
        return super(UploadNewFile, self).form_invalid(form)


class ListUploadedFiles(ListView):
    """ This class view would list all the csv files the user has uploaded """
    template_name = 'documents/list_files.html'
    context_object_name = 'files'

    def get_queryset(self):
        return UploadedFile.objects.all()


class UpdateUploadedFile(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """ This class view would update an already uploaded file """

    template_name = 'documents/update_file.html'
    queryset = UploadedFile.objects.all()
    form_class = CSVFileUploadForm
    context_object_name = 'csv_file'
    permission_denied_message = 'You are not authorized to view this page'

    def get_object(self, queryset=None):
        return UploadedFile.objects.get(id=self.kwargs['id'])

    def has_permission(self):
        current_obj = self.get_object()
        return self.request.user == current_obj.uploaded_by

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Successfully updated the file!')
        return reverse('accounts:all_files')


class DetailUploadedFile(DetailView):
    """ This view would render uploaded file details in bar chart form """

    queryset = UploadedFile.objects.all()
    template_name = 'documents/detail_file.html'
    context_object_name = 'file_object'

    def get_object(self, queryset=None):
        return UploadedFile.objects.get(id=self.kwargs['id'])


class DeleteUploadedFile(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """ This class view would delete an uploaded file """
    template_name = 'documents/delete_file.html'
    queryset = UploadedFile.objects.all()
    context_object_name = 'file_object'

    def get_success_url(self):
        return reverse('accounts:all_files')

    def get_object(self, queryset=None):
        return UploadedFile.objects.get(id=self.kwargs['id'])

    def has_permission(self):
        current_obj = self.get_object()
        return self.request.user == current_obj.uploaded_by