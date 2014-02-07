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

BEFORE=False
OS="Mac OS X"
STARTING_DAY = datetime(2014,2,6,tzinfo=pytz.timezone('US/Pacific'))
END_DAY = datetime(2014,2,7,tzinfo=pytz.timezone('US/Pacific'))
LOAD_FROM_PKL=False

if len(sys.argv) == 2:
    fname_prefix=sys.argv[1]
else: fname_prefix='dfl'

if fname_prefix == 'osx':
    OS="Mac OS X"
elif fname_prefix == 'ios':
    OS="Apple iOS"
elif fname_prefix == 'android':
    OS="Android"
else:
    fname_prefix="Mac OS X"

class UnknownTransitionError(Exception):
    pass

class FSM(object):
    def __init__(self, init_state):
        self.state = init_state
        self.inputs = []
        self.states = []
        self.transitions = {}

    def add_transition(self, state, input, action, next_state):
        self.transitions[(input,state)] = {'handler':action, 'next_state':next_state}

    def get_transition(self, input, state):
        try:
            transition = self.transitions[(input,state)]
        except KeyError:
            print "Unknown Transition Requested : %s, %s" % (input, state)
            raise UnknownTransitionError
            transition = None
        return transition

    def processFSM(self, state, input, *args):
        transition = self.get_transition(input, state)
        if transition == None:
            return
        if transition['handler']:
            transition['handler'](*args)
        self.state = transition['next_state']
        return self.state

class SessionFSM(FSM):
    def __init__(self):
        self.states = ['IDLE','ON_BEHOP','ON_LWAPP']
        self.inputs = ['AssocReq','ReassocReq','Deauth','HostTimeout','ASSOC_RESP','REASSOC_RESP']
        self.sessions = []
        self.start_event = None
        self.intermediate = None

        FSM.__init__(self, 'IDLE')
        self.add_transition('IDLE','AssocReq',self.start_session,'ON_BEHOP')
        self.add_transition('IDLE','ReassocReq',self.start_session,'ON_BEHOP')
        self.add_transition('IDLE','ASSOC_RESP',self.start_session,'ON_LWAPP')
        self.add_transition('IDLE','REASSOC_RESP',self.start_session,'ON_LWAPP')
        self.add_transition('IDLE','DEAUTH',None,'IDLE')
        self.add_transition('IDLE','DisassocReq',None,'IDLE')
        self.add_transition('IDLE','HostTimeout',None,'IDLE')
        self.add_transition('ON_BEHOP','AssocReq',self.behop_to_behop,'ON_BEHOP')
        self.add_transition('ON_BEHOP','ReassocReq',self.behop_to_behop,'ON_BEHOP')
        self.add_transition('ON_BEHOP','ASSOC_RESP',self.behop_to_lwapp,'ON_LWAPP')
        self.add_transition('ON_BEHOP','REASSOC_RESP',self.behop_to_lwapp,'ON_LWAPP')
        self.add_transition('ON_BEHOP','DisassocReq',self.behop_disassoc,'IDLE')
        self.add_transition('ON_BEHOP','DeauthReq',self.behop_deauth,'IDLE')
        self.add_transition('ON_BEHOP','HostTimeout',self.behop_timeout,'IDLE')
        self.add_transition('ON_BEHOP','DEAUTH',None,'ON_BEHOP')
        self.add_transition('ON_LWAPP','AssocReq',self.lwapp_to_behop,'ON_BEHOP')
        self.add_transition('ON_LWAPP','ReassocReq',self.lwapp_to_behop,'ON_BEHOP')
        self.add_transition('ON_LWAPP','ASSOC_RESP',self.lwapp_to_lwapp,'ON_LWAPP')
        self.add_transition('ON_LWAPP','REASSOC_RESP',self.lwapp_to_lwapp,'ON_LWAPP')
        self.add_transition('ON_LWAPP','DEAUTH',self.lwapp_deauth,'IDLE')
        self.add_transition('ON_LWAPP','DisassocReq',self.add_intermediate,'ON_LWAPP')
        self.add_transition('ON_LWAPP','HostTimeout',self.add_intermediate,'ON_LWAPP')
        self.add_transition('ON_LWAPP','DeauthReq',self.add_intermediate,'ON_LWAPP')

    def add_intermediate(self, event):
        self.intermediate = event

    def behop_to_lwapp(self, event):
        self.restart_session(event, reason = 'behop_to_lwapp')

    def lwapp_to_behop(self, event):
        self.restart_session(event, reason= 'lwapp_to_behop')

    def behop_to_behop(self, event):
        self.restart_session(event, reason = 'behop_to_behop')

    def lwapp_to_lwapp(self, event):
        self.restart_session(event, reason = 'lwapp_to_lwapp')

    def behop_disassoc(self, event):
        self.close_session(event, reason = 'behop_disassoc')

    def behop_deauth(self, event):
        self.close_session(event, reason = 'behop_deauth')

    def behop_timeout(self, event):
        self.close_session(event, reason = 'behop_timeout')

    def lwapp_deauth(self, event):
        self.close_session(event, reason = 'lwapp_deauth')

    def start_session(self, event):
        self.start_event = event
        if event.event_signal in ['AssocReq','ReassocReq']:
            self.enter_reason = 'idle->behop'
        elif event.event_signal in ['ASSOC_RESP','REASSOC_RESP']:
            self.enter_reason = 'idle->lwapp'

    def close_session(self, event, reason=None):
        self.sessions.append({'start':self.start_event.timestamp,'end':event.timestamp,'client':event.client,
                              'sig':event.event_signal,'dur':event.timestamp - self.start_event.timestamp,
                              'reason':reason,'intermediate':None,'enter_reason':self.enter_reason})
        self.start_event = None
        self.enter_reason = None

    def restart_session(self, event,reason=None):
        if self.intermediate:
            intermediate={'sig':self.intermediate.event_signal,'timestamp':self.intermediate.timestamp}
        else:
            intermediate=None
        self.sessions.append({'start':self.start_event.timestamp,'end':event.timestamp,'client':event.client,
                              'sig':event.event_signal,'dur':event.timestamp - self.start_event.timestamp,
                              'reason':reason,'intermediate':intermediate, 'enter_reason':self.enter_reason})
        self.start_event = event
        self.enter_reason = reason
        self.intermediate = None


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
    #pylab.yscale('log')
    pylab.xlabel('Time')
    pylab.ylabel('Session Duration (secs)')
    #pylab.legend(loc=3)
    
    #pylab.savefig(fname)

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
    #plt.gca().set_yticks([0,10,100,1000,10000])
    #plt.gca().set_yticklabels([0,10,100,1000,10000])
    pylab.xlim([tick_dates[0],tick_dates[-1]])
    #pylab.ylim([-10, 10000])
    #pylab.yscale('log')
    pylab.xlabel('Day')
    pylab.ylabel('# of sessions')
    pylab.title("# of sessions/day (%s)" % (label))
    #pylab.legend(loc=3)
    
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
    #pylab.legend(loc=3)

    #pylab.savefig('/tmp/%s_clients.png' % prefix)
    

def load_sessions_from_file(fname):
    
    f = open(fname,'rb')
    sessions = pickle.load(f)
    f.close()
    return sessions

def load_sessions_from_db():
    '''
    Returns a dictionary with sessions for every client.
    Each client's sessions are a time-ordered list.
    '''
    interesting_behop_events = ['HostTimeout','AssocReq','ReassocReq','DisassocReq','DeauthReq']
    interesting_lwapp_events = ['DEAUTH','REASSOC_RESP','ASSOC_RESP']
    clients = Client.objects.filter(location='S6',os=OS)
    behop_events = EventLog.objects.filter(location='S6',
                                           event_signal__in=interesting_behop_events,
                                           client__in=[client.mac_address for client in clients],
                                           timestamp__gt=STARTING_DAY,
                                           timestamp__lt=END_DAY).order_by('timestamp')
    
    lwapp_events = EventLog.objects.filter(location='S6',
                                           event_signal__in=interesting_lwapp_events,
                                           client__in=[client.mac_address for client in clients],
                                           timestamp__gt=STARTING_DAY,
                                           timestamp__lt=END_DAY).order_by('timestamp')

    combined_events = [b for b in behop_events] + [l for l in lwapp_events]
    combined_events = sorted(combined_events, key=lambda e:e.timestamp)


    print "Got all events from DB"
    all_events = defaultdict(list)
    for e in combined_events:
        all_events[e.client].append(e)

    all_sessions = {}
    print "Building WiFi sessions for %d clients" % len(clients)
    for client in all_events.keys():
        events = all_events[client]
        fsm = SessionFSM()
        cur_state = 'IDLE'
        for e in events:
            new_state = fsm.processFSM(cur_state,e.event_signal,e)
            cur_state = new_state
        all_sessions[client] = sorted(fsm.sessions,key=lambda s:s['start'])
    all_sessions = build_session_details(all_sessions)
    return all_sessions


def session_breakdown(sessions):
    cnt = Counter()
    for s in sessions:
        cnt[s['type']] += 1
    #print "Total sessions : %d" % len(sessions)
    #print "\n".join([str(i) for i in cnt.items()])
    return cnt

def get_usage_client(client):
    ip_address = Client.objects.get(mac_address=client).ip_address
    transfer = TransferLog.objects.filter(location='S5',client=ip_address,
                                          timestamp__gt=STARTING_DAY,
                                          timestamp__lt=END_DAY).order_by('timestamp')
    in_bytes = sum([t.in_bytes for t in transfer])
    out_bytes = sum([t.out_bytes for t in transfer])
    return (in_bytes,out_bytes)


def get_usage(clients):
    data_transfer = defaultdict(list)
    for client in clients:
        data_transfer[client] = get_usage_client(client)
    return data_transfer

def build_client_session_details(sessions):
    ss = sorted(sessions, key=lambda s:s['start'])
    # start by fixing the types of session (should do when building the FSM)
    for s in ss:
        if s['enter_reason'] in ('idle->behop','lwapp_to_behop','behop_to_behop'):
            s['type'] = 'behop'
        else:
            s['type'] = 'lwapp'
    for i in range(1,len(ss)-1):
        ss[i]['prev'] = ss[i-1]['type']
        ss[i]['next'] = ss[i+1]['type']
        ss[i]['prev_dur'] = ss[i-1]['dur']
        ss[i]['next_dur'] = ss[i+1]['dur']
    return ss
        
def build_session_details(sessions):
    for cl in sessions.keys():
        sessions[cl] = build_client_session_details(sessions[cl])
    return sessions

def get_flat_sessions(sessions):
    all_sessions = []
    for cl in sessions.keys():
        all_sessions += sessions[cl]
    return all_sessions

def plot_cdf(lists,fname,xlogscale=False,ylogscale=False,title=''):
    pylab.figure()
    for l in lists:
        x = sorted(l[0])
        y = [float(i)/len(x) for i in range(len(x))]
        pylab.plot(x,y,label=l[1])
    pylab.grid()
    pylab.legend()
    if xlogscale:
        pylab.xscale('log')
    pylab.title(title)
    pylab.savefig(fname)

def dump_to_file(l,fname):
    f = open(fname,'wb')
    pickle.dump(l,f)
    f.close()

def plot_sessions_durations(sessions,prefix=fname_prefix):
    # Plot duration of behop/lwapp sessions
    behop_sessions = [s for s in sessions if s['type'] == 'behop']
    lwapp_sessions = [s for s in sessions if s['type'] == 'lwapp']
    to_plot = [([s['dur'].total_seconds() for s in behop_sessions],'behop (%d)' % len(behop_sessions)),
               ([s['dur'].total_seconds() for s in lwapp_sessions],'lwapp (%d)' % len(lwapp_sessions))]
    plot_cdf(to_plot,fname='session_duration_all_%s' % prefix,
             xlogscale=True,title='Duration for all sessions (%s)' % prefix)


    # Plot duration based on the transition
    transition_reasons = set([s['reason'] for s in sessions])
    for reason in transition_reasons:
        ss = [s for s in sessions if s['reason'] == reason]
        if len(ss) == 1 and ss[0]['dur'].total_seconds() < 1: # single entry with zero value throws an error..
            continue
        to_plot = [([s['dur'].total_seconds() for s in ss],'%s (%d)' % (reason,len(ss)))]
        plot_cdf(to_plot,fname='session_duration_%s_%s' % (reason,prefix),
                 xlogscale=True,title='Duration for reason %s (%s)' % (reason,prefix))

def plot_session_timeline(sessions,prefix=fname_prefix):
    offset = {'behop':1,'lwapp':2 }
    annot = {'behop':'b-*','lwapp':'r-*'}
    pylab.figure()
    for s in sessions:
        pylab.plot([s['start'],s['end']],[offset[s['type']],offset[s['type']]], annot[s['type']])
    pylab.xlim((STARTING_DAY,END_DAY))
    pylab.ylim([0,3])
    pylab.savefig('%s_timeline' % (prefix))

if __name__=='__main__':
    if LOAD_FROM_PKL == False:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE','behop_dashboard.settings')
        from logs.models import Client,TransferLog, RttLog, NetflixLog,YoutubeLog,EventLog
        db_clients = Client.objects.filter(location='S5',os=OS)
        sessions = load_sessions_from_db()
        data_transfers = get_usage(sessions.keys())
        dump_to_file(sessions,'sessions_%s.pkl' % fname_prefix)
        dump_to_file(data_transfers,'data_%s.pkl' % fname_prefix)

    else:
        sessions = load_sessions_from_file('sessions.pkl')
        data_transfers = load_transfers_from_file('data.pkl')

    clients = sessions.keys()
    flat_sessions = get_flat_sessions(sessions)
    plot_sessions_durations(flat_sessions)
    for cl in clients:
        plot_sessions_durations(sessions[cl],"%s_%s" % (fname_prefix,cl))
        plot_session_timeline(sessions[cl],"%s_%s" % (fname_prefix,cl))

    for cl in clients:
        breakdown = session_breakdown(sessions[cl])
        _cl = Client.objects.get(mac_address=cl)
        print "Breakdown for client %s (%s|%s)\t: Total: %3d BeHop: %3d LWAPP: %3d Transfer (%d/%d)" % \
            (cl, _cl.user,_cl.type,len(sessions[cl]),breakdown['behop'],breakdown['lwapp'],
             data_transfers[cl][0]/2**20,data_transfers[cl][1]/2**20)
    breakdown = session_breakdown(flat_sessions)
    print "Breakdown for aggregate : Total: %3d BeHop: %3d LWAPP: %3d" % (len(flat_sessions),
                                                                          breakdown['behop'],
                                                                          breakdown['lwapp'])

        
    sys.exit(0)
    #sys.exit(0)
    #lwapp_sessions = analyze_s4_sessions()
    #combined_sessions = behop_sessions + lwapp_sessions
    sessions = defaultdict(list)
    for s in combined_sessions:
        sessions[s['client']].append(s)

    # Get usage for each client of interest
    for client in sessions.keys():
        sessions[client] = sorted(sessions[client],key=lambda s:s['start'])
    clients = sorted(sessions.keys(), key=lambda c:data_transfer[c][0])
    f = open('/tmp/%s_data_transfer_%s.pkl' % (fname_prefix,OS),'wb')
    f1 = open('/tmp/%s_sessions_%s.pkl' % (fname_prefix,OS),'wb')
    pickle.dump(data_transfer,f)
    pickle.dump(sessions,f1)
    f.close()
    f1.close()
