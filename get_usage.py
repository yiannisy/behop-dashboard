#!/usr/bin/env python
import os,sys
from datetime import datetime,timedelta
from time import time
import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz
from collections import defaultdict

if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','behop_dashboard.settings')
    from logs.models import Client,TransferLog, RttLog, NetflixLog,YoutubeLog,EventLog
    starting = datetime(2014,3,1,tzinfo=pytz.timezone('US/Pacific'))
    ending = datetime(2014,3,14,tzinfo=pytz.timezone('US/Pacific'))
    switch = datetime(2014,1,24,tzinfo=pytz.timezone('US/Pacific'))

    n_logs = TransferLog.objects.filter(location='S5',timestamp__gt=starting)
    input = []
    output = []

    output = defaultdict(list)
    
    for l in n_logs:
        output[(l.timestamp - starting).days].append(l)
    dates = output.keys()
                    
    pylab.figure()
    pylab.plot_date(matplotlib.dates.date2num([starting + timedelta(days=d) for d in dates]),
                    [sum([l.in_bytes for l in output[d]]) for d in dates],'b.',label='in')
    pylab.plot_date(matplotlib.dates.date2num([starting + timedelta(days=d) for d in dates]),
                    [sum([l.out_bytes for l in output[d]]) for d in dates],'r.',label='out')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    tick_dates = [starting + timedelta(days=i) for i in range(0,max(dates),max(dates)/8)]
    plt.gca().set_xticks(tick_dates)
    #plt.gca().set_yticks([0,10,100,1000,10000])
    #plt.gca().set_yticklabels([0,10,100,1000,10000])
    pylab.xlim([starting,ending])
    #pylab.ylim([-10, 10000])
    pylab.yscale('log')
    pylab.xlabel('Time')
    pylab.ylabel('Traffic served (bytes)')
    pylab.legend(loc=3)
    pylab.grid()
    pylab.title("Traffic Served")
    pylab.savefig('/tmp/usage.png')

