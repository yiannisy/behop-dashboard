#!/usr/bin/env python
import os
from datetime import datetime

def last_seen(obj):
    tstamp = None
    rtt_logs = TransferLog.objects.filter(client=obj.ip_address).order_by('-timestamp')
    if len(rtt_logs) > 0:
        tstamp = rtt_logs[0].timestamp
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

def bytes_dl(obj):
    transfer_logs = TransferLog.objects.filter(client=obj.ip_address)
    return sum([log.in_bytes for log in transfer_logs])/float(2**20)

def bytes_upl(obj):
    transfer_logs = TransferLog.objects.filter(client=obj.ip_address)
    return sum([log.out_bytes for log in transfer_logs])/float(2**20)

if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','behop_dashboard.settings')
    from logs.models import Client,TransferLog, RttLog, NetflixLog,YoutubeLog
    for client in Client.objects.all():
        client.last_seen = last_seen(client)
        client.netflix_mins = netflix_mins(client)
        client.youtube_mins = youtube_mins(client)
        client.rtt_samples = rtt_samples(client)
        client.pkts_dl = pkts_dl(client)
        client.pkts_upl = pkts_upl(client)
        client.bytes_dl = bytes_dl(client)
        client.bytes_upl = bytes_upl(client)
        print "Updated Client %s" % client.ip_address
        client.save()

