from django.views.generic import FormView, ListView, UpdateView, DeleteView, DetailView
from . forms import CSVFileUploadForm
from . models import UploadedFile
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from . serializers import ViewDocumentSerializer, UploadedFileSerializer
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from rest_framework.permissions import IsAuthenticated
import csv


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


class ListUploadedFiles(LoginRequiredMixin, ListView):
    """ This class view would list all the csv files the user has uploaded """
    template_name = 'documents/list_files.html'
    context_object_name = 'files'

    def get_queryset(self):
        try:
            filter_text = self.request.GET['file_description_text']
            return UploadedFile.objects.filter(uploaded_by=self.request.user, file_description__icontains=filter_text)
        except:
            # Simply return all objects when no query params are found and exception is raised
            return UploadedFile.objects.filter(uploaded_by=self.request.user)


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


class DetailUploadedFile(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    """ This view would render uploaded file details in bar chart form """

    queryset = UploadedFile.objects.all()
    template_name = 'documents/detail_file.html'
    context_object_name = 'file_object'

    def get_object(self, queryset=None):
        return UploadedFile.objects.get(id=self.kwargs['id'])

    def has_permission(self):
        current_obj = self.get_object()
        return self.request.user == current_obj.uploaded_by

    def get_context_data(self, **kwargs):
        context = super(DetailUploadedFile, self).get_context_data(**kwargs)
        uploaded_file_obj = self.get_object()
        uploaded_csv_file = uploaded_file_obj.uploaded_file
        file_data = []
        try:
            with open(uploaded_csv_file.path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    file_data.append(row)
                context['csv_headers'] = [item.upper() for item in file_data[0]]
                context['file_data'] = file_data[1:]
        except Exception as err:
            print(err)
        return context


class DeleteUploadedFile(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """ This class view would delete an uploaded file """
    template_name = 'documents/delete_file.html'
    queryset = UploadedFile.objects.all()
    context_object_name = 'file_object'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Successfully deleted the file!')
        return reverse('accounts:all_files')

    def get_object(self, queryset=None):
        return UploadedFile.objects.get(id=self.kwargs['id'])

    def has_permission(self):
        current_obj = self.get_object()
        return self.request.user == current_obj.uploaded_by


class GetAllDocumentsAPI(APIView):
    permission_classes = []

    def get(self, request):
        try:
            all_user_documents = UploadedFile.objects.filter(uploaded_by_id=request.user.id)
            document_data = ViewDocumentSerializer(all_user_documents, many=True).data
            return Response({'message': 'All documents fetched', 'data': document_data}, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response({'message': 'Failed to fetch user documents'}, status=status.HTTP_400_BAD_REQUEST)


class GetDocumentDetail(APIView):
    permission_classes = []

    def get(self, request, pk):
        try:
            session_data = []
            page_data = []
            date_data = []
            document = UploadedFile.objects.get(id=pk)
            uploaded_csv_file = document.uploaded_file
            with open(uploaded_csv_file.path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    session_data.append(row[3])
                    page_data.append(row[2])
                    date_data.append(row[1])

            document_data = ViewDocumentSerializer(document).data
            return Response({'message': 'Document fetched', 'data': document_data,
                             'csv_data': {
                                 'date_data': date_data[1:],
                                 'page_data': page_data[1:],
                                 'session_data': session_data[1:]
                             }}, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response({'message': 'Failed to fetch user document'}, status=status.HTTP_400_BAD_REQUEST)


class UploadFileAPIView(CreateAPIView):
    """ API for uploading CSV document """
    serializer_class = UploadedFileSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validatedData = serializer.validated_data
            instance = self.perform_create(serializer)
            return Response(
                {'message': 'You have been successfully uploaded file.', 'success': True, 'data': serializer.data},
                status=status.HTTP_201_CREATED)
        except Exception as err:
            print(err)
            return Response({'message': 'Failed to upload file, some error occurred!', 'errors': serializer.errors, 'success': False},
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # Update user password here
        return serializer.save(uploaded_by=self.request.user)


class DeleteFileAPIView(DestroyAPIView):
    """ API for deleting CSV document """
    serializer_class = UploadedFileSerializer
    permission_classes = [IsAuthenticated]
    queryset = UploadedFile.objects.all()

    def get_object(self):
        return UploadedFile.objects.get(id=self.kwargs['id'])

    def preform_destroy(self, instance):
        if instance.uploaded_by_id != self.request.user.id:
            raise ValueError("Not authorized to delete this object.")
        return instance.delete()


class GetCSVDocumentView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, id):
        try:
            csv_file_obj = UploadedFile.objects.get(id=id)
            csv_data = []
            with open(csv_file_obj.uploaded_file.path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    csv_data.append(row)
            return Response(
                {'message': 'Successfully fetched CSV data for this file.', 'success': True, 'data': csv_data},
                status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return Response({'message': 'Failed to fetch csv data, some error occurred!', 'success': False},
                            status=status.HTTP_400_BAD_REQUEST)


class UpdateFileAPIView(UpdateAPIView):
    """ API for updating an uploaded file """
    serializer_class = UploadedFileSerializer
    permission_classes = [IsAuthenticated,]
    queryset = UploadedFile.objects.all()

    def get_object(self):
        uploaded_file_obj = UploadedFile.objects.get(id=self.kwargs['id'])
        return uploaded_file_obj

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        except Exception as err:
            print(err)
            return Response({'message': 'Failed to update file, some error occurred!', 'errors': serializer.errors,
                             'success': False},
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class GetDocumentDetailView(RetrieveAPIView):
    serializer_class = ViewDocumentSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return UploadedFile.objects.get(id=self.kwargs['id'])


