from django.core.management.base import BaseCommand, CommandError
from main.models import Consultation
import datetime
import requests
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Updates the parlimantary schedule via the parliament website'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        message = 'results: '
        url = 'https://www.gov.uk/government/publications.atom?publication_filter_option=consultations'
        try:
            r  = requests.get(url)
        except:
            r = False
            message += 'request failed. '
        if r:
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
            entries = soup.findAll('entry')
            dupes = 0
            for entry in entries:
                gov_id = entry.find('id')
                gov_id = "".join(gov_id.strings)
                if Consultation.objects.filter(gov_id=gov_id).exists():
                    dupes += 1
                    message += "%s dupes. " % dupes
                else:
                    date = entry.find('published')
                    date = "".join(date.strings)
                    date = date[:-6]
                    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
                    title = entry.find('title')
                    title = "".join(title.strings)
                    summary = entry.find('summary')
                    summary = "".join(summary.strings)
                    url = entry.find('link')
                    url = str(url.href)
                    c = Consultation(gov_id = gov_id, date=date, title = title, summary = summary, url = url)
                    c.save()
                    message += "Added a consultation: %s" % title
        self.stdout.write(self.style.SUCCESS(message))
