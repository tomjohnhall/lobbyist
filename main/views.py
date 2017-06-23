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
from models import Event, Consultation
from collections import defaultdict



def index(request):
    todaydate = datetime.date.today()
    schedule = Event.objects.order_by('date', 'house', 'location')
    consultations = Consultation.objects.order_by('-date')
    if 'postcode' in request.session:
        postcode = request.session['postcode']
        return render(request, 'index.html', {'postcode': postcode, 'schedule': schedule, 'todaydate': todaydate, 'consultations':consultations})
    else:
        return render(request, 'index.html', {'schedule': schedule, 'todaydate': todaydate})


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

def petitions(request):
    try:
        send_url = 'http://petition.parliament.uk/petitions.json?state=all'
        r = requests.get(send_url)
        data = json.loads(r.text)
    except:
        data = {'error_message':'Connection error. Retry.'}
    return JsonResponse(data, safe=False)
