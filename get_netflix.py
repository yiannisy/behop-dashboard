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
    clients = Client.objects.filter(os="Mac OS X").values('ip_address').distinct()
    clients = [cl.values()[0] for cl in clients]
    print clients
    n_requests = NetflixLog.objects.filter(location='S5',client__in=clients,rate__gt=0)
    n_rates = sorted([req.rate for req in n_requests])
    x = n_rates
    y = [(float(i + 1) / len(x)) for i in range(len(x))]

    m_requests = NetflixLog.objects.filter(location='S6',client__in=clients,rate__gt=0)
    m_rates = sorted([req.rate for req in m_requests])
    z = m_rates
    w = [(float(i + 1) / len(z)) for i in range(len(z))]


    pylab.figure()
    pylab.plot(x,y,label='S5')
    pylab.plot(z,w,label='S6')
    pylab.grid()
    pylab.legend()
    pylab.axis([0,10000,0,1])
    pylab.xlabel('Rate (Kbps)')
    pylab.ylabel('CDF')
    pylab.title('CDF for Youtube Rate.')
    pylab.savefig('/tmp/youtube_s5.png')
    
    
