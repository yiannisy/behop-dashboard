#!/usr/bin/env python
import os
from datetime import datetime,timedelta
from time import time
import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz

if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','behop_dashboard.settings')
    from logs.models import Client,TransferLog, RttLog, NetflixLog,YoutubeLog,EventLog
    starting = datetime(2014,1,4,tzinfo=pytz.UTC)
    ending = datetime.today() + timedelta(days=2)
    switch = datetime(2014,1,24,tzinfo=pytz.UTC)

    n_logs = TransferLog.objects.filter(location='S5')
    input = []
    output = []
    for i in range(starting.day,ending.day):
        dt_start = datetime(2014,1,i,8,tzinfo=pytz.UTC)
        dt_end = datetime(2014,1,i+1,8,tzinfo=pytz.UTC)
        in_bytes = sum([log.in_bytes for log in n_logs if log.timestamp > dt_start and log.timestamp < dt_end])
        out_bytes = sum([log.out_bytes for log in n_logs if log.timestamp > dt_start and log.timestamp < dt_end])
        input.append(in_bytes)
        output.append(out_bytes)
                    
    pylab.figure()
    pylab.plot(matplotlib.dates.date2num([datetime(2014, 1,i, tzinfo=pytz.UTC) 
                                          for i in range(starting.day,ending.day)]),input,'b.',label='in')
    pylab.plot(matplotlib.dates.date2num([datetime(2014, 1,i, tzinfo=pytz.UTC) 
                                          for i in range(starting.day,ending.day)]),output,'r.',label='out')
    pylab.axvline(switch)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    tick_dates = [datetime(2014,01,i) for i in range(starting.day,ending.day, (ending.day-starting.day)/8)]
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

