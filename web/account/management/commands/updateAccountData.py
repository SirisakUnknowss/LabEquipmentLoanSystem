from datetime import time
import json
# Django
from django.core.management.base import BaseCommand, CommandError
# Project
from account.models import Account


class Command(BaseCommand):
    
    help = "Update prefix and levelClass in All Accounts."

    def handle(self, *args, **options):
        try:
            with open('./account/management/commands/output_data.json', 'r', encoding='utf-8') as f:
                data_list = json.load(f)
            for entry in data_list:
                print(entry['prefix'])
                print(entry['levelClass'])
                account = Account.objects.get(id=entry['id'])
                account.prefix = entry['prefix']
                account.levelClass = entry['levelClass']
                account.save(update_fields=["prefix", "levelClass"])
                self.stdout.write(self.style.SUCCESS(f'{account.studentID} Update Complete!'))
            self.stdout.write(self.style.SUCCESS('Update All Complete!'))
        except Exception as error:
            raise CommandError("Error: {}".format(error))