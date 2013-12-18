from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.core import serializers
import string
import json
from datetime import datetime
#from django.views.generic.simple import direct_to_template

from models import Client, NetflixLog, YoutubeLog, RttLog

# Create your views here.
def show_stats(request):
    '''
    Basic view to show statistics for a given list of clients.
    Clients are a pk list in the GET request. From this we extract
    the IP addresses from clients, and then get the desired log entries
    for Netflix,Youtube, and RTT.
    Return a page with basic graphs.
    '''
    client_ids = string.split(request.GET.get('clients'),',')
    clients = Client.objects.filter(pk__in=client_ids)
    ip_address = [client.ip_address for client in clients]
    netflix_logs = NetflixLog.objects.filter(client__in=ip_address, timestamp__gt=datetime(2013,2,1))
    netflix_rates = [{'ip_address':log.client,'rate':log.rate,'tstamp':str(log.timestamp)} 
                     for log in netflix_logs]
    netflix_rates = json.dumps(netflix_rates)

    youtube_logs = YoutubeLog.objects.filter(client__in=ip_address, timestamp__gt=datetime(2013,2,1))
    youtube_rates = [{'ip_address':log.client, 'rate':log.rate,'tstamp':str(log.timestamp)}
                     for log in youtube_logs]
    youtube_rates = json.dumps(youtube_rates)

    rtt_logs = RttLog.objects.filter(client__in=ip_address)
    rtt = [{'ip_address':log.client, 'rtt':log.rtt,'tstamp':str(datetime.fromtimestamp(log.timestamp))}           
           for log in rtt_logs]
    rtt = json.dumps(rtt)

    return render(request, 'logs/stats.html',{'netflix':netflix_rates,'youtube':youtube_rates,'rtt':rtt})
