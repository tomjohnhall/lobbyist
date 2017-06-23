from django.core.management.base import BaseCommand, CommandError
from main.models import Event
import datetime
import requests
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Updates the parlimantary schedule via the parliament website'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        message = 'Result: '
        today = datetime.date.today()
        old = (today - datetime.timedelta(days=10))
        events = Event.objects.all()
        for event in events:
            x = 0
            if event.date < old:
                event.delete()
                x+=1
                message += '%s old events removed. ' % x
        def getEvents(url, house, message):
            try:
                r  = requests.get(url)
            except:
                r = False
                message += 'request failed. '
            if r:
                data = r.text
                soup = BeautifulSoup(data, 'html.parser')
                tds = soup.findAll('td')
                dupes = 0
                for td in tds:
                    title = td.find('p', {'class': 'parl-calendar-event-title'})
                    if title:
                        title = str(title)
                        description = td.find('p', {'class': 'parl-calendar-event-description'})
                        description = str(description)
                        location = td.findParents('table')[0]['data-specflow-id']
                        location = str(location)
                        date = today
                        event = Event(date=date, location=location, house=house, title=title, description=description)
                        if Event.objects.filter(date=date, title=title, house=house).exists():
                            dupes += 1
                            message = 'duplicates %s' % dupes
                        else:
                            event.save()
                    else:
                        message += 'no events. '
        for n in range(10):
            year = today.strftime('%Y')
            month = today.strftime('%m')
            day = today.strftime('%d')
            commons_url = 'https://calendar.parliament.uk/calendar/Commons/All/' + year + '/' + month + '/' + day + '/Daily'
            lords_url ='https://calendar.parliament.uk/calendar/Lords/All/' + year + '/' + month + '/' + day + '/Daily'
            getEvents(commons_url, 'House of Commons', message)
            getEvents(lords_url, 'House of Lords', message)
            today += datetime.timedelta(days=1)
        message += "successfully updated schedule."
        self.stdout.write(self.style.SUCCESS(message))
