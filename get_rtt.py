#!/usr/bin/env python
import os
from datetime import datetime
from time import time
import matplotlib
matplotlib.use('Agg')
import pylab

if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','behop_dashboard.settings')
    from logs.models import Client,TransferLog, RttLog, NetflixLog,YoutubeLog,EventLog
    pylab.figure()
    for device in ["Mac OS X","Apple iOS","Android"]:
        clients = Client.objects.filter(os=device).values('ip_address').distinct()
        clients = [cl.values()[0] for cl in clients]
        print clients
        n_requests = RttLog.objects.filter(location='S5',client__in=clients)
        n_rtt = sorted([req.rtt for req in n_requests])
        x = n_rtt
        y = [(float(i + 1) / len(x)) for i in range(len(x))]
        pylab.plot(x,y,label='%s' % (device))

    pylab.grid()
    pylab.legend()
    pylab.xscale('log')
    pylab.xlabel('rtt (ms)')
    pylab.ylabel('CDF')
    pylab.title('CDF for RTT Logs.')
    pylab.savefig('/tmp/rtt_s5.png')
    
    
