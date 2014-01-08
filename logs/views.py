from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.core import serializers
import string
import json
from datetime import datetime
from time import time
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

    since_secs = time() -  63*24*60*60

    netflix_logs = NetflixLog.objects.filter(client__in=ip_address, rate__gt=100,
                                             timestamp__gt=datetime.fromtimestamp(since_secs))
    netflix_rates = [{'ip_address':log.client,'rate':log.rate,'tstamp':str(log.timestamp)} 
                     for log in netflix_logs]
    netflix_rates = json.dumps(netflix_rates)

    youtube_logs = YoutubeLog.objects.filter(client__in=ip_address, 
                                             timestamp__gt=datetime.fromtimestamp(since_secs))
    youtube_rates = [{'ip_address':log.client, 'rate':log.rate,'tstamp':str(log.timestamp)}
                     for log in youtube_logs]
    youtube_rates = json.dumps(youtube_rates)
    
    rtt_logs = RttLog.objects.filter(client__in=ip_address, timestamp__gt=since_secs)
    rtt = [{'ip_address':log.client, 'rtt':log.rtt,'tstamp':str(datetime.fromtimestamp(log.timestamp))}           
           for log in rtt_logs]
    rtt = json.dumps(rtt)

    #netflix_sum = {}
    #for log in netflix_logs:
    #    netflix_sum[log.ip_address]

    summary = {'rtt_samples':len(rtt_logs), 'netflix_samples':len(netflix_logs),
               'netflix_dur':sum([log.dur for log in netflix_logs])/(1000*60.0),
               'youtube_samples':len(youtube_logs)}

    return render(request, 'logs/stats.html',{'netflix':netflix_rates,'youtube':youtube_rates,
                                              'rtt':rtt, 'summary':summary})
