from django.core.management.base import BaseCommand, CommandError
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'This Management Command would delete all the existing user accounts.'

    def handle(self, *args, **options):
        all_users = CustomUser.objects.all()
        for each_user in all_users:
            try:
                current_user_name = each_user.username
                each_user.delete()
            except CustomUser.DoesNotExist:
                raise CommandError('User does not exist')
            self.stdout.write(self.style.SUCCESS('This user was successfully deleted %s ' % current_user_name))