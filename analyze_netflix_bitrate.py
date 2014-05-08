#!/usr/bin/env python

import os
from datetime import datetime,timedelta
import time
import sys
import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz
from collections import defaultdict, Counter
import pickle
from util import *

OS="Mac OS X"
#OS="Apple iOS"
#OS="Android"
STARTING_DAY = datetime(2014,2,20,20,tzinfo=pytz.timezone('US/Pacific'))
FINAL_DAY = datetime(2014,2,25,tzinfo=pytz.timezone('US/Pacific'))


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='BeHop dashboard offline analysis tool.')
    parser.add_argument('--sday', default=None, type=int, nargs='+',help='Starting date (YYYY MM DD)')
    parser.add_argument('--fday', default=None, type=int, nargs='+',help='Final date (YYYY MM DD)')

    args = parser.parse_args()

    if args.sday:
        starting_day = datetime(sday[0],sday[1],sday[2],tzinfo=pytz.timezone('US/Pacific'))
    else:
        starting_day = STARTING_DAY

    if args.fday:
        final_day = datetime(fday[0],fday[1],fday[2],tzinfo=pytz.timezone('US/Pacific'))
    else:
        final_day = FINAL_DAY
                                

    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','behop_dashboard.settings')
    from logs.models import Client,BandwidthLog,NetflixBitrateLog
    db_clients = Client.objects.filter(location='S5',os=OS).values('ip_address').distinct()
    clients =[cl.values()[0] for cl in db_clients]

    b_logs = NetflixBitrateLog.objects.filter(location='S5',client__in=clients,timestamp__gt=STARTING_DAY,
                                         timestamp__lt=END_DAY)

    all_logs = []
    for client in clients:
        b_log = [b for b in b_logs if b.client == client]
        b_log = sorted(b_log,key=lambda b:b.timestamp)
        for i in range(2,len(b_log) - 1):
            if ((b_log[i].timestamp - b_log[i-1].timestamp) < timedelta(seconds=65)) and ((b_log[i+1].timestamp - b_log[i].timestamp) < timedelta(seconds=65)):
                all_logs.append(b_log[i])
        #print len(b_log), len(all_logs)

    to_plot = [([b.bitrate_down for b in all_logs],'in'),
               ([b.bitrate_up for b in all_logs],'out')]
    plot_cdf(to_plot,fname='bandwidth',xlim=[10**4,10**8],
             xlogscale=True,title='Netflix bitrate for BeHop (OSX)',
             xlabel='bps',ylabel='CDF')
