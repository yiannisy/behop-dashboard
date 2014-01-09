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

from models import *

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
    mac_address = [client.mac_address for client in clients]

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

    transfer_logs = TransferLog.objects.filter(client__in=ip_address, timestamp__gt=datetime.fromtimestamp(since_secs))
    activity_logs = [{'ip_address':log.client, 'bytes_dl':log.in_bytes,'bytes_upl':log.out_bytes,
                      'tstamp':log.timestamp.isoformat()}
                     for log in transfer_logs]
    activity_logs = json.dumps(activity_logs)

    event_logs = EventLog.objects.filter(client__in=mac_address, timestamp__gt=datetime.fromtimestamp(since_secs))
    event_logs = [{'mac_address':log.client, 'event_name':log.event_name,'signal':log.signal,
                   'tstamp':log.timestamp.isoformat()}
                  for log in event_logs]
    categories = set([e['event_name'] + '<->'+e['signal'] for e in event_logs])
    print categories
    _event_logs = {}
    for category in categories:
        print category
        _event_logs[category] = [e for e in event_logs if e['event_name'] + '<->'+e['signal'] == category]
    event_logs = json.dumps(_event_logs)

    #netflix_sum = {}
    #for log in netflix_logs:
    #    netflix_sum[log.ip_address]

    summary = {'rtt_samples':len(rtt_logs), 'netflix_samples':len(netflix_logs),
               'netflix_dur':sum([log.dur for log in netflix_logs])/(1000*60.0),
               'youtube_samples':len(youtube_logs)}

    return render(request, 'logs/stats.html',{'netflix':netflix_rates,'youtube':youtube_rates,
                                              'events':event_logs,
                                              'activity':activity_logs,'rtt':rtt, 'summary':summary})
