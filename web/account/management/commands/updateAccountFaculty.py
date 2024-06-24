from datetime import time
import json
# Django
from django.core.management.base import BaseCommand, CommandError
# Project
from account.models import Account


class Command(BaseCommand):
    
    help = "Update faculty in Other faculty of Accounts."

    def handle(self, *args, **options):
        try:
            accounts = Account.objects.filter(faculty="Other")
            for account in accounts:
                print(account.faculty)
                account.faculty = "other"
                account.save(update_fields=["faculty"])
                self.stdout.write(self.style.SUCCESS(f'{account.studentID} Update Complete!'))
            self.stdout.write(self.style.SUCCESS('Update All Complete!'))
        except Exception as error:
            raise CommandError("Error: {}".format(error))