#!/usr/bin/env python
import os
from datetime import datetime
from time import time

DAY_SECS = 24*60*60

def last_seen(obj):
    tstamp = None
    rtt_logs = TransferLog.objects.filter(client=obj.ip_address).order_by('-timestamp')
    if len(rtt_logs) > 0:
        tstamp = rtt_logs[0].timestamp
    return tstamp

def last_heard(obj):
    tstamp = None
    event_logs = EventLog.objects.filter(client=obj.mac_address, category='WiFi',location='S5').order_by('-timestamp')
    if len(event_logs) > 0:
        tstamp = event_logs[0].timestamp
    return tstamp

def last_detected(obj, band=None):
    tstamp = None
    if band:
        event_logs = EventLog.objects.filter(client=obj.mac_address, category='Monitor',band=band).order_by('-timestamp')
    else:
        event_logs = EventLog.objects.filter(client=obj.mac_address, category='Monitor').order_by('-timestamp')
    if len(event_logs) > 0:
        tstamp = event_logs[0].timestamp
    return tstamp

def netflix_mins(obj):
    netflix_logs = NetflixLog.objects.filter(client=obj.ip_address,rate__gt=100)
    dur = sum([log.dur for log in netflix_logs])/(1000*60.0)
    return dur

def youtube_mins(obj):
    youtube_logs = YoutubeLog.objects.filter(client=obj.ip_address, rate__gt=100)
    dur = sum([log.dur for log in youtube_logs])/(1000*60.0)
    return dur

def rtt_samples(obj):
    return RttLog.objects.filter(client=obj.ip_address).count()

def pkts_dl(obj):
    transfer_logs = TransferLog.objects.filter(client=obj.ip_address)
    return sum([log.in_pkts for log in transfer_logs])

def pkts_upl(obj):
    transfer_logs = TransferLog.objects.filter(client=obj.ip_address)
    return sum([log.out_pkts for log in transfer_logs])

def bytes_dl(obj, since_secs=None):
    if since_secs:
        since = time() - since_secs
    else:
        since = 0
    transfer_logs = TransferLog.objects.filter(client=obj.ip_address, 
                                               timestamp__gt=datetime.fromtimestamp(since))
    return sum([log.in_bytes for log in transfer_logs])/float(2**20)

def bytes_upl(obj, since_secs=None):
    if since_secs:
        since = time() - since_secs
    else:
        since = 0
    transfer_logs = TransferLog.objects.filter(client=obj.ip_address, 
                                               timestamp__gt=datetime.fromtimestamp(since))
    return sum([log.out_bytes for log in transfer_logs])/float(2**20)

if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','behop_dashboard.settings')
    from logs.models import Client,TransferLog, RttLog, NetflixLog,YoutubeLog,EventLog
    for client in Client.objects.filter(location='S5'):
        client.last_seen = last_seen(client)
        client.last_heard = last_heard(client)
        #client.last_detected = last_detected(client)
        #client.last_detected_2GHz = last_detected(client,band='2.4GHz')
        #client.last_detected_5GHz = last_detected(client,band='5GHz')
        #client.netflix_mins = netflix_mins(client)
        #client.youtube_mins = youtube_mins(client)
        #client.rtt_samples = rtt_samples(client)
        #client.pkts_dl = pkts_dl(client)
        #client.pkts_upl = pkts_upl(client)
        #client.bytes_dl = bytes_dl(client)
        #client.bytes_upl = bytes_upl(client)
        client.bytes_dl_last = bytes_dl(client, since_secs = DAY_SECS)
        client.bytes_upl_last = bytes_upl(client, since_secs = DAY_SECS)

        print "Updated Client %s" % client.ip_address
        client.save()

