#!/usr/bin/env python
import os
from datetime import datetime
import time
import sys
import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz

BEFORE=False

def plot_sessions(sessions, fname, switch):
    pylab.figure()
    pylab.plot_date(matplotlib.dates.date2num([s['end'] for s in sessions if s['sig'] == 'DisassocReq']),
                    [s['dur'] for s in sessions if s['sig'] == 'DisassocReq'],
                    'b.',label='disassoc')
    pylab.plot_date(matplotlib.dates.date2num([s['end'] for s in sessions if s['sig'] == 'DeauthReq']),
                    [s['dur'] for s in sessions if s['sig'] == 'DeauthReq'],
                    'r.',label='deauth')
    pylab.plot_date(matplotlib.dates.date2num([s['end'] for s in sessions if s['sig'] == 'HostTimeout']),
                    [s['dur'] for s in sessions if s['sig'] == 'HostTimeout'],
                    'g.',label='timeout')
    pylab.axvline(switch)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    tick_dates = [datetime(2014,01,i) for i in range(17,28)]
    plt.gca().set_xticks(tick_dates)
    plt.gca().set_yticks([0,10,100,1000,10000])
    plt.gca().set_yticklabels([0,10,100,1000,10000])
    pylab.xlim([tick_dates[0],tick_dates[-1]])
    pylab.ylim([-10, 10000])
    pylab.yscale('log')
    pylab.xlabel('Time')
    pylab.ylabel('Session Duration (secs)')
    pylab.legend(loc=3)
    
    pylab.savefig(fname)




if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','behop_dashboard.settings')
    from logs.models import Client,TransferLog, RttLog, NetflixLog,YoutubeLog,EventLog
    clients = Client.objects.filter(os="Mac OS X",location='S5').values('mac_address').distinct()
    clients = [cl.values()[0] for cl in clients]
    print clients
    print len(clients)
    all_sessions = {}
    for client in clients:
        starting = datetime(2014,1,17,8,tzinfo=pytz.UTC)
        switch = datetime(2014,1,24,8,tzinfo=pytz.UTC)
        until = datetime.now()
        sessions = []
        events = EventLog.objects.filter(client=client, 
                                         timestamp__gt=starting,
                                         timestamp__lt=until).order_by('timestamp')        
        if len(events) == 0:
            continue
        start = events[0].timestamp
        start_ts = time.mktime(start.timetuple())
        for e in events:
            if e.signal == "AssocReq" or e.signal == "ReassocReq":
                start = e.timestamp
                start_ts = time.mktime(e.timestamp.timetuple())
            if e.signal == "DisassocReq" or e.signal == "DeauthReq":
                end = e.timestamp
                end_ts = time.mktime(e.timestamp.timetuple())
                sessions.append({'end':end,'start':start,'dur':end_ts-start_ts,'sig':e.signal})
            # remove 300sec offset for hosttimeout.
            if e.signal == "HostTimeout":
                end = e.timestamp
                end_ts = time.mktime(e.timestamp.timetuple()) - 300
                sessions.append({'end':end,'start':start,'dur':end_ts-start_ts,'sig':e.signal})
        if len(sessions) == 0:
            continue

        plot_sessions(sessions,'/tmp/client_%s.png' % client, switch)

        #print "\n".join(["%d %s -> %s (%s)" % (s['dur'],s['start'],s['end'],s['sig']) for s in sessions])
        #print "\n".join(["%s:%s" % (e.timestamp,e.signal) for e in events])
        
        all_sessions[client] = sessions
        

    sessions = []
    for s in all_sessions.values():
        sessions += s
    pre_sessions = [s for s in sessions if s['end'] < switch]
    post_sessions = [s for s in sessions if s['end'] > switch]
    pre_sessions = sorted(pre_sessions, key=lambda s:s['dur'])
    post_sessions = sorted(post_sessions, key=lambda s:s['dur'])
    sessions = sorted(sessions, key=lambda s:s['dur'])
    plot_sessions(sessions, '/tmp/client_all.png',switch)
    timeout_pre_sessions = [s for s in pre_sessions if s['sig'] == "HostTimeout"]
    disassoc_pre_sessions = [s for s in pre_sessions if s['sig'] != "HostTimeout"]
    timeout_post_sessions = [s for s in post_sessions if s['sig'] == "HostTimeout"]
    disassoc_post_sessions = [s for s in post_sessions if s['sig'] != "HostTimeout"]

    print "Total Sessions : %d ( avg dur : %d, med dur : %d )" % \
        (len(sessions),
         sum([s['dur'] for s in sessions])/len(sessions),
         sessions[len(sessions)/2]['dur'])
    print "Timeout Pre-Sessions : %d ( avg dur : %d, med dur : %d )" % \
        (len(timeout_pre_sessions),
         sum([s['dur'] for s in timeout_pre_sessions])/len(timeout_pre_sessions),
         timeout_pre_sessions[len(timeout_pre_sessions)/2]['dur'])
    print "Disassoc Pre-Sessions : %d ( avg dur : %d, med dur : %d )" % \
        (len(disassoc_pre_sessions),
         sum([s['dur'] for s in disassoc_pre_sessions])/len(disassoc_pre_sessions),
         disassoc_pre_sessions[len(disassoc_pre_sessions)/2]['dur'])

    print "Timeout Post-Sessions : %d ( avg dur : %d, med dur : %d )" % \
        (len(timeout_post_sessions),
         sum([s['dur'] for s in timeout_post_sessions])/len(timeout_post_sessions),
         timeout_post_sessions[len(timeout_post_sessions)/2]['dur'])
    print "Disassoc Post-Sessions : %d ( avg dur : %d, med dur : %d )" % \
        (len(disassoc_post_sessions),
         sum([s['dur'] for s in disassoc_post_sessions])/len(disassoc_post_sessions),
         disassoc_post_sessions[len(disassoc_post_sessions)/2]['dur'])

  
    pylab.figure()
    for ss in [(timeout_pre_sessions,'timeout-pre'),(timeout_post_sessions, 'timeout-post')]:
        x = sorted([s['dur'] for s in ss[0]])
        y = [float(i)/len(x) for i in range(0,len(x))]
        pylab.plot(x,y,label=ss[1])
    pylab.legend(loc=4)
    pylab.xscale('log')
    pylab.grid()
    pylab.xlabel('Session Duration (secs)')
    pylab.ylabel('CDF')
    pylab.savefig('/tmp/client_timeout_cdf.png')

    pylab.figure()
    for ss in [(disassoc_pre_sessions,'disassoc-pre'),(disassoc_post_sessions, 'disassoc-post')]:
        x = sorted([s['dur'] for s in ss[0]])
        y = [float(i)/len(x) for i in range(0,len(x))]
        pylab.plot(x,y,label=ss[1])
    pylab.legend(loc=4)
    pylab.xscale('log')
    pylab.grid()
    pylab.xlabel('Session Duration (secs)')
    pylab.ylabel('CDF')
    pylab.savefig('/tmp/client_disassoc_cdf.png')

    pylab.figure()
    for ss in [(pre_sessions,'pre'),(post_sessions, 'post')]:
        x = sorted([s['dur'] for s in ss[0]])
        y = [float(i)/len(x) for i in range(0,len(x))]
        pylab.plot(x,y,label=ss[1])
    pylab.legend(loc=4)
    pylab.xscale('log')
    pylab.grid()
    pylab.xlabel('Session Duration (secs)')
    pylab.ylabel('CDF')
    pylab.savefig('/tmp/client_cdf.png')
