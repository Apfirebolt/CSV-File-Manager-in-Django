from django.shortcuts import render
from django.views.generic import FormView, ListView, UpdateView, DeleteView, DetailView


class UploadNewFile(FormView):
    """ This class would upload a new file using form """
    pass


class ListUploadedFiles(ListView):
    """ This class view would list all the csv files the user has uploaded """
    pass


class UpdateUploadedFile(UpdateView):
    """ This class view would update an already uploaded file """
    pass


class DetailUploadedFile(DetailView):
    """ This view would render uploaded file details in bar chart form """
    pass


class DeleteUploadedFile(DeleteView):
    """ This class view would delete an uploaded file """
    pass