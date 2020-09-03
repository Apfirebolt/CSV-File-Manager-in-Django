from django.shortcuts import render


def handler404(request, exception):
   return render(request, '404.html')


def handler403(request, exception):
   return render(request, '403.html')


def handler500(request, exception):
   return render(request, '500.html')


def handler400(request, exception):
   return render(request, '400.html')