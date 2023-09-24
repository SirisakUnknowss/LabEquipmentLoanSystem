from datetime import time
# Django
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
# Project
from scientificInstrument.models import ScientificInstrument, Booking


class Command(BaseCommand):
    
    help = "Check booking and update time."

    def handle(self, *args, **options):
        try:
            for booking in Booking.objects.all():
                print(booking.timeBooking)
                try:
                    timeStart = int(booking.timeBooking.split(":")[0])
                except Exception as error: continue
                booking.startBooking = time(timeStart, 0)
                booking.endBooking = time(timeStart +1, 0)
                booking.save()
                self.stdout.write(self.style.SUCCESS(f'{booking.pk} Update Complete!'))
            self.stdout.write(self.style.SUCCESS('Update All Complete!'))
        except Exception as error:
            raise CommandError("Error: {}".format(error))