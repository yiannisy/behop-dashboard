#!/usr/bin/env python
import os
from datetime import datetime
from time import time

if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','behop_dashboard.settings')
    from logs.models import Client,TransferLog, RttLog, NetflixLog,YoutubeLog,EventLog
    all_clients = Client.objects.values('ip_address').distinct()
    clients = [cl.values()[0] for cl in all_clients]
    #n_clients = NetflixLog.objects.filter(location='S6').values('client').distinct()
    #y_clients = YoutubeLog.objects.filter(location='S6').values('client').distinct()
    #clients = []
    #for cl in n_clients:
    #    clients = clients + cl.values()
    #for cl in y_clients:
    #    clients = clients + cl.values()
    clients = sorted(set(clients))
    print "\n".join(clients)
