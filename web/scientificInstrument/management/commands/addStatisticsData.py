from datetime import time
# Django
from django.core.management.base import BaseCommand, CommandError
# Project
from borrowing.models import Order
from scientificInstrument.models import ScientificInstrument, Booking


class Command(BaseCommand):
    
    help = "Check booking and update time."

    def handle(self, *args, **options):
        try:
            for booking in Booking.objects.filter(status=Order.STATUS.APPROVED):
                booking.scientificInstrument.statistics += 1
                booking.scientificInstrument.save(update_fields=['statistics'])
                self.stdout.write(self.style.SUCCESS(f'{booking.pk} Update Complete!'))
            self.stdout.write(self.style.SUCCESS('Update All Complete!'))
        except Exception as error:
            raise CommandError("Error: {}".format(error))