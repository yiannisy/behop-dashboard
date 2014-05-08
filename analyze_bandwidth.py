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
STARTING_DAY = datetime(2014,2,21,20,tzinfo=pytz.timezone('US/Pacific'))
END_DAY = datetime(2014,2,25,tzinfo=pytz.timezone('US/Pacific'))


if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','behop_dashboard.settings')
    from logs.models import Client,BandwidthLog
    db_clients = Client.objects.filter(location='S5',os=OS).values('ip_address').distinct()
    clients =[cl.values()[0] for cl in db_clients]

    b_logs = BandwidthLog.objects.filter(location='S5',client__in=clients,timestamp__gt=STARTING_DAY,
                                         timestamp__lt=END_DAY)

    print len(b_logs)

    to_plot = [([b.in_avgrate_bps for b in b_logs],'in'),
               ([b.out_avgrate_bps for b in b_logs],'out')]
    plot_cdf(to_plot,fname='bandwidth',xlim=[1,10**9],
             xlogscale=True,title='bitrate for BeHop')
