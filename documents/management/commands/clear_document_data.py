from django.core.management.base import BaseCommand, CommandError
from documents.models import UploadedFile


class Command(BaseCommand):
    help = 'This Management Command would delete all the uploaded files.'

    def handle(self, *args, **options):
        all_files = UploadedFile.objects.all()
        for each_file in all_files:
            try:
                current_file_name = each_file.file_description
                each_file.delete()
            except UploadedFile.DoesNotExist:
                raise CommandError('Associated File Does Not Exist.')
            self.stdout.write(self.style.SUCCESS('This file was successfully deleted %s ' % current_file_name))