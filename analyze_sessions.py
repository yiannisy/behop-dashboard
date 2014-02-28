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

def plot_daily_session_summary(sessions, since=None, prefix=None,label=''):
    if since == None:
        since = datetime(2014,1,25,tzinfo=pytz.UTC)
    d_sessions = defaultdict(list)
    for s in sessions:
        d_sessions[(s['end'] - since).days].append(s)
    dates = d_sessions.keys()

    pylab.figure()
    pylab.plot_date(matplotlib.dates.date2num([since + timedelta(days=d) for d in dates]),
                    [len(d_sessions[d]) for d in dates])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    tick_dates = [since + timedelta(days=i) for i in range(max(dates))]
    plt.gca().set_xticks(tick_dates)
    plt.gca().set_yticks([0,10,100,1000,10000])
    plt.gca().set_yticklabels([0,10,100,1000,10000])
    pylab.xlim([tick_dates[0],tick_dates[-1]])
    pylab.ylim([-10, 10000])
    pylab.yscale('log')
    pylab.xlabel('Day')
    pylab.ylabel('# of sessions')
    pylab.title("# of sessions/day (%s)" % (label))
    pylab.legend(loc=3)
    
    pylab.savefig('/tmp/%s_sum.png' % prefix)


    pylab.figure()
    pylab.plot_date(matplotlib.dates.date2num([since + timedelta(days=d) for d in dates]),
                    [len(set([s['client'] for s in d_sessions[d]])) for d in dates])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    tick_dates = [since + timedelta(days=i) for i in range(max(dates))]
    plt.gca().set_xticks(tick_dates)
    #plt.gca().set_yticks([0,10,100,1000,10000])
    #plt.gca().set_yticklabels([0,10,100,1000,10000])
    pylab.xlim([tick_dates[0],tick_dates[-1]])
    #pylab.ylim([-10, 10000])
    #pylab.yscale('log')
    pylab.xlabel('Day')
    pylab.ylabel('# of clients')
    pylab.title("# of clients/day (%s)" % (label))
    pylab.legend(loc=3)

    pylab.savefig('/tmp/%s_clients.png' % prefix)
    

def analyze_s5_sessions():
    interesting_events = ['HostTimeout','AssocReq','ReassocReq','DisassocReq','DeauthReq']
    clients = EventLog.objects.filter(location='S5',event_signal__in=interesting_events).values('client').distinct()
    s5_events = EventLog.objects.filter(location='S5',event_signal__in=interesting_events).order_by('timestamp')

    print "Got all events from DB"
    all_events = defaultdict(list)
    for e in s5_events:
        all_events[e.client].append(e)
    print "Sorted per client"

    clients = [c['client'] for c in clients]
    all_sessions = []
    print "WiFi events for %d clients" % len(clients)
    for client in all_events.keys():
        events = all_events[client]
        on_session = False
        sessions = []
        for e in events:
            if ((on_session == False) and (e.event_signal == 'AssocReq' or e.event_signal == 'ReassocReq')):
                start = e.timestamp
                on_session = True
                continue
            if ((on_session == True) and (e.event_signal == 'DisassocReq' or e.event_signal == 'DeauthReq' or e.event_signal == 'HostTimeout')):
                end = e.timestamp
                on_session = False
                if e.event_signal == 'HostTimeout':
                    reason = 'timeout'
                    end = end - timedelta(minutes=5)
                else:
                    reason = 'disassoc'
                if (end != None) and (start != None):
                    sessions.append({'end':end,'start':start,'dur':end-start,'sig':e.event_signal,
                                     'client':client,'reason':reason})
        all_sessions += sessions

    plot_daily_session_summary(all_sessions,prefix='s5',label='Studio 5')
    
    all_durs = sorted([s['dur'].total_seconds() for s in all_sessions])
    all_durs_disassoc = sorted([s['dur'].total_seconds() for s in all_sessions if s['reason'] == 'disassoc'])
    all_durs_timeout = sorted([s['dur'].total_seconds() for s in all_sessions if s['reason'] == 'timeout'])
    print "Total Sessions Detected : %d" % len(all_durs)
    print "Avg Session Duration %f" % (sum(all_durs)/len(all_durs))
    print "Median Session Duration %f" % (all_durs[len(all_durs)/2])
    
    pylab.figure()
    for x,label in ((all_durs,'all'),(all_durs_disassoc,'disassoc'),(all_durs_timeout,'timeout')):
        y = [float(i)/len(x) for i in range(0,len(x))]
        pylab.plot(x,y,label=label)
    pylab.title("Session Duration (Studio 5)")
    pylab.grid()
    pylab.xlabel("Duration (secs)")
    pylab.ylabel("CDF")
    pylab.xscale('log')
    pylab.legend()
    pylab.savefig("/tmp/studio5_sessions_cdf.png")

    pylab.figure()
    client_sessions = [s['client'] for s in all_sessions]
    clients = set(client_sessions)
    count_sessions = []
    print "Anallyzing count for %d clients" % len(clients)
    for client in clients:
        count_sessions.append(client_sessions.count(client))

    pylab.figure()
    x = sorted(count_sessions)
    y = [float(i)/len(x) for i in range(0,len(x))]
    pylab.plot(x,y)
    pylab.title("Session Count per Client (Studio 5)")
    pylab.grid()
    pylab.xlabel("# of Sessions")
    pylab.ylabel("CDF")
    pylab.xscale('log')
    pylab.savefig("/tmp/studio5_sessions_count_cdf.png")



def analyze_s6_sessions():
    clients = EventLog.objects.filter(location='S6').values('client').distinct()
    s6_events = EventLog.objects.filter(location='S6').order_by('timestamp')
    clients = [c['client'] for c in clients]
    all_sessions = []
    print "Got all S6 events from DB"
    all_events = defaultdict(list)
    for e in s6_events:
        all_events[e.client].append(e)
    print "Sorted per client"
    print "WiFi events for %d clients" % len(clients)
    for client in all_events.keys():
        events = all_events[client]
        on_session = False
        sessions = []
        for e in events:
            if ((on_session == False) and (e.event_signal == 'ASSOC_RESP' or e.event_signal == 'REASSOC_RESP' or e.event_name == 'ASSOC_RESP' or e.event_name == 'REASSOC_RESP')):
                start = e.timestamp
                on_session = True
                continue
            if ((on_session == True) and (e.event_signal == 'ASSOC_RESP' or e.event_signal == 'REASSOC_RESP' or e.event_name == 'ASSOC_RESP' or e.event_name == 'REASSOC_RESP' or e.event_name == 'DEAUTH' or e.event_signal == 'DEAUTH')):
                end = e.timestamp
                on_session = False
                if e.event_name == 'unknown':
                    sig = e.event_signal
                else:
                    sig = e.event_name
                if sig == 'DEAUTH':
                    reason = 'deauth'
                else:
                    reason = 'roam'
                sessions.append({'end':end,'start':start,'dur':end-start,'sig':sig,'client':client,'reason':reason})
        all_sessions += sessions

    plot_daily_session_summary(all_sessions,prefix='s6',label='Studio 6')

    all_durs = sorted([s['dur'].total_seconds() for s in all_sessions])
    all_durs_deauth = sorted([s['dur'].total_seconds() for s in all_sessions if s['reason'] == 'deauth'])
    all_durs_roam = sorted([s['dur'].total_seconds() for s in all_sessions if s['reason'] == 'roam'])
    print "Total Sessions Detected : %d" % len(all_durs)
    print "Avg Session Duration %f" % (sum(all_durs)/len(all_durs))
    print "Median Session Duration %f" % (all_durs[len(all_durs)/2])
    
    pylab.figure()
    for x,label in ((all_durs,'all'),(all_durs_deauth,'deauth'),(all_durs_roam,'roam')):
        y = [float(i)/len(x) for i in range(0,len(x))]
        pylab.plot(x,y,label=label)
    pylab.title("Session Duration (Studio 6)")
    pylab.grid()
    pylab.xlabel("Duration (secs)")
    pylab.ylabel("CDF")
    pylab.xscale('log')
    pylab.legend()
    pylab.savefig("/tmp/studio6_sessions_cdf.png")

    pylab.figure()
    client_sessions = [s['client'] for s in all_sessions]
    count_sessions = []
    for client in clients:
        count_sessions.append(client_sessions.count(client))

    pylab.figure()
    x = sorted(count_sessions)
    y = [float(i)/len(x) for i in range(0,len(x))]
    pylab.plot(x,y)
    pylab.title("Session Count per Client (Studio 6)")
    pylab.grid()
    pylab.xlabel("# of Sessions")
    pylab.ylabel("CDF")
    pylab.xscale('log')
    pylab.savefig("/tmp/studio6_sessions_count_cdf.png")



if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','behop_dashboard.settings')
    from logs.models import Client,TransferLog, RttLog, NetflixLog,YoutubeLog,EventLog
    starting = datetime(2014, 1, 4)
    #plot_daily_session_summary([],starting,"test")
    analyze_s5_sessions()
    analyze_s6_sessions()
