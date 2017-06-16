from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
import csv
import os
import datetime
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static



def index(request):
    if 'postcode' in request.session:
        postcode = request.session['postcode']
        return render(request, 'index.html', {'postcode': postcode})
    else:
        return render(request, 'index.html')


def postcode(request):
    mp = {}
    partyImages = {
    'conservative': static('img/conservative.png'),
    'labour': static('img/labour.png'),
    'scottish': static('img/snp.png'),
    'liberal': static('img/libdem.png'),
    'unionist': static('img/dup.png'),
    'sinn': static('img/sinnfein.png'),
    'plaid': static('img/plaidcymru.png'),
    'green': static('img/green.png'),
    'independent': static('img/other.png'),
    'ulster': static('img/ulster.png'),
    'social': static('img/sdlp.png'),
    'independence': static('img/ukip.png'),
    'other': static('img/other.png'),
    }
    if request.method == 'POST':
        postcode = request.POST.get('postcode')
        postcode = str(postcode)
        postcode = postcode.replace(' ', '')
        postcode = postcode.lower()
        mpurl = 'https://www.theyworkforyou.com/api/getMP?postcode=' + postcode + '&key=DNuDaHEVykaGFi7Yh5DNYz8K&output=js'
        try:
            r = requests.get(mpurl)
            mpresponse = json.loads(r.text)
        except:
            mpresponse = {'error': 'connection error'}
            mp = mpresponse
            return JsonResponse(mp, safe=False)
        if 'error' not in mpresponse:
            name = mpresponse['full_name']
            everyPolitician = os.path.join(settings.BASE_DIR, 'static', 'term-57.csv')
            with open(everyPolitician, 'rb') as f:
                reader = csv.reader(f)
                contact = None
                for row in reader:
                    if row[1] == name:
                        email = row[3]
                        twitter = row[4]
                        facebook = row[5]
                        image = row[14]
                        contact = {'email':email,'twitter':twitter,'facebook':facebook}
            if image:
                mpresponse['image'] = image
            mp['details'] = mpresponse
            mp['contact'] = contact
            party = {}
            party['name'] = mpresponse['party']
            lowparty = mpresponse['party'].lower()
            for key, value in partyImages.items():
                if key in lowparty:
                    party['image'] = value
                    break
                else:
                    party['image'] = partyImages['other']
            mp['party'] = party
            request.session['postcode'] = postcode
            return JsonResponse(mp, safe=False)
        else:
            mp = mpresponse
            return JsonResponse(mp, safe=False)
    else:
        return HttpResponseRedirect(reverse_lazy('main:index'))

def clearPostcode(request):
    del request.session['postcode']
    clear = True
    if 'postcode' in request.session:
        clear = False
    return JsonResponse(clear, safe=False)

def upcomingParliament(request):
    schedule = []
    today = datetime.date.today()
    todaystr = today.strftime('the day is %d and the month is %m and the year is %Y')
    def getEvents(url):
        try:
            r  = requests.get(url)
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')
            tds = soup.findAll('td')
            events = []
            for td in tds:
                title = td.find('p', {'class': 'parl-calendar-event-title'}).getText()
                if title:
                    event = {}
                    event['title'] = str(title)
                    event['description'] = str(td.find('p', {'class': 'parl-calendar-event-description'}))
                    event['type'] = str(td.findParents('table')[0]['data-specflow-id'])
                    events.append(event)
            return events
        except:
            pass
    for n in range(20):
        schedule.append({'date': today.strftime('%d/%m/%Y')})
        year = today.strftime('%Y')
        month = today.strftime('%m')
        day = today.strftime('%d')
        commons_url = 'https://calendar.parliament.uk/calendar/Commons/All/' + year + '/' + month + '/' + day + '/Daily'
        lords_url ='https://calendar.parliament.uk/calendar/Lords/All/' + year + '/' + month + '/' + day + '/Daily'
        schedule[n]['commons_events'] = getEvents(commons_url)
        schedule[n]['lords_events'] = getEvents(lords_url)
        today += datetime.timedelta(days=1)
    return JsonResponse(schedule, safe=False)
