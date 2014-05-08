#!/usr/bin/env python

import os
from datetime import datetime,timedelta
import time
import sys
import pytz
from collections import defaultdict, Counter
import pickle
from util import *
import argparse
import logging
import matplotlib
matplotlib.use('Agg')
import pylab as plt
import numpy as np

OS_ABBRV = {'osx':'Mac OS X','ios':'Apple iOS','android':'Android'}
STARTING_DAY = datetime(2014,2,20,20,tzinfo=pytz.timezone('US/Pacific'))
FINAL_DAY = datetime(2014,2,25,tzinfo=pytz.timezone('US/Pacific'))

logging.basicConfig(format='%(message)s')

os.environ.setdefault('DJANGO_SETTINGS_MODULE','behop_dashboard.settings')
from logs.models import Client,BandwidthLog,NetflixBitrateLog,TransferLog,YoutubeBitrateLog

def analyze_bandwidth(clients):
    '''Analyze bitrate logs for studio 5 clients.
    '''
    bitrate_logs = BandwidthLog.objects.filter(timestamp__gt=starting_day,timestamp__lt=final_day,
                                               client__in=clients)
    total_bitrates = {'lwapp':0,'behop':0}
    logging.warning("============= Bandwidth ===============")
    logging.warning("Client\tLWAPP mins\tBeHop mins")
    bitrates = {}
    
    for client in sorted(clients):
        _cl_bitrates = []
        client_bitrates = [log for log in bitrate_logs if log.client == client]
        client_bitrates = sorted(client_bitrates,key=lambda b:b.timestamp)
        for i in range(2,len(client_bitrates) -1):
            if ((client_bitrates[i].timestamp - client_bitrates[i-1].timestamp) < timedelta(seconds=65)) and ((client_bitrates[i+1].timestamp - client_bitrates[i].timestamp) < timedelta(seconds=65)):
                _cl_bitrates.append(client_bitrates[i])
        client_bitrates = _cl_bitrates
        lwapp_bitrates = [log.in_avgrate_bps/1000 for log in client_bitrates if log.location == 'S4']
        behop_bitrates = [log.in_avgrate_bps/1000 for log in client_bitrates if log.location == 'S5']
        bitrates[client] = {'lwapp':lwapp_bitrates,'behop':behop_bitrates}
        total_bitrates['lwapp'] += len(lwapp_bitrates)
        total_bitrates['behop'] += len(behop_bitrates)

        logging.warning("%s\t%d\t%d" % (client,len(lwapp_bitrates),len(behop_bitrates)))


    logging.warning("Total LWAPP : %d | Total BeHop : %d" % (total_bitrates['lwapp'],total_bitrates['behop']))
    lwapp = []
    behop = []
    to_plot = []
    for client in clients:        
        lwapp += bitrates[client]['lwapp']
        behop += bitrates[client]['behop']
        to_plot.append((bitrates[client]['lwapp'],'lwapp','r'))
        to_plot.append((bitrates[client]['behop'],'behop','b'))
    plot_cdf(to_plot,'bandwidth_bitrates',legend=False,xlogscale=True,title='Bandwidth bitrates',alpha=0.3)
    to_plot = []
    to_plot.append((lwapp,'lwapp','r'))
    to_plot.append((behop,'behop','b'))
    plot_cdf(to_plot,'bw_aggregate_bitrates',legend=True,xlogscale=True,title='bw bitrates')


def analyze_video_bitrate(clients,service):
    '''Analyze bitrate logs for studio 5 clients.
    '''
    if service == 'netflix':
        bitrate_logs = NetflixBitrateLog.objects.filter(timestamp__gt=starting_day,timestamp__lt=final_day,
                                                        client__in=clients)
    elif service == 'youtube':
        bitrate_logs = YoutubeBitrateLog.objects.filter(timestamp__gt=starting_day,timestamp__lt=final_day,
                                                        client__in=clients)
        

    pktrates = {}
    total_bitrates = {'lwapp':0,'behop':0}
    logging.warning("==============Service %s===============" % service)
    logging.warning("Client\tLWAPP mins\tBeHop mins")
    
    for client in sorted(clients):
        _cl_bitrates = []
        client_bitrates = [log for log in bitrate_logs if log.client == client and log.bitrate_down > 1000]
        client_bitrates = sorted(client_bitrates,key=lambda b:b.timestamp)
        for i in range(2,len(client_bitrates) -1):
            if ((client_bitrates[i].timestamp - client_bitrates[i-1].timestamp) < timedelta(seconds=65)) and ((client_bitrates[i+1].timestamp - client_bitrates[i].timestamp) < timedelta(seconds=65)):
                _cl_bitrates.append(client_bitrates[i])

        tmp_cls = []
        concatenated_bitrates = []
        for cl in _cl_bitrates:
            if len(tmp_cls) == 0:
                tmp_cls.append(cl)
            elif tmp_cls[0].timestamp.minute == cl.timestamp.minute:
                tmp_cls.append(cl)
            else:
                tmp_cls[0].bitrate_down = sum([l.bitrate_down for l in tmp_cls])
                concatenated_bitrates.append(tmp_cls[0])
                tmp_cls = []
                tmp_cls.append(cl)

        client_bitrates = concatenated_bitrates
        lwapp_pktrates = [log.bitrate_down/1000.0 for log in client_bitrates if log.location == 'S4']
        behop_pktrates = [log.bitrate_down/1000.0 for log in client_bitrates if log.location == 'S5']
        pktrates[client] = {'lwapp':lwapp_pktrates,'behop':behop_pktrates}
        total_bitrates['lwapp'] += len(lwapp_pktrates)
        total_bitrates['behop'] += len(behop_pktrates)

    for client in sorted(clients,key=lambda c:(len(pktrates[c]['lwapp']) + len(pktrates[c]['behop']))):
        if len(pktrates[client]['lwapp']) + len(pktrates[client]['behop']) > 0:
            logging.warning("%s\t%d\t%d" % (client,len(pktrates[client]['lwapp']),len(pktrates[client]['behop'])))


    logging.warning("Total LWAPP : %d | Total BeHop : %d" % (total_bitrates['lwapp'],total_bitrates['behop']))
    lwapp = []
    behop = []
    to_plot = []
    for client in clients:        
        lwapp += pktrates[client]['lwapp']
        behop += pktrates[client]['behop']
        to_plot.append((pktrates[client]['lwapp'],'lwapp','r'))
        to_plot.append((pktrates[client]['behop'],'behop','b'))
    plot_cdf(to_plot,'%s_bitrates' % service ,legend=False,xlogscale=True,alpha=0.3,title='%s bitrates' % service)
    to_plot = []
    to_plot.append((lwapp,'lwapp','r'))
    to_plot.append((behop,'behop','b'))
    plot_cdf(to_plot,'%s_aggregate_bitrates' % service ,legend=True,xlogscale=True,title='%s bitrates' % service)

def analyze_traffic_breakdown():
    total_bytes = {}
    db_clients = BandwidthLog.objects.filter(timestamp__gt=starting_day,timestamp__lt=final_day).values('client').distinct()
    clients =[cl.values()[0] for cl in db_clients]
    total_bytes['alluser'] = analyze_transfers(clients)
    dyn_clients = [cl for cl in clients if cl.startswith("10.30.8") or cl.startswith("10.30.9")]
    total_bytes['dynuser'] = analyze_transfers(dyn_clients)
    res_clients = [cl for cl in clients if cl.startswith("10.30.6") or cl.startswith("10.30.7")]
    total_bytes['resuser'] = analyze_transfers(res_clients)
    other_clients = [cl for cl in clients if not 
               (cl.startswith("10.30.6") or cl.startswith("10.30.7") 
                or cl.startswith("10.30.8") or cl.startswith("10.30.9"))]
    total_bytes['otheruser'] = analyze_transfers(other_clients)
    db_clients = Client.objects.filter(location__in=args.loc,os__in=client_os).values('ip_address').distinct()
    behop_clients =[cl.values()[0] for cl in db_clients]
    behop_clients = [cl for cl in behop_clients if cl in clients]
    total_bytes['behopuser'] = analyze_transfers(behop_clients)

    all_bytes = total_bytes['alluser']['lwapp_dl'] + total_bytes['alluser']['behop_dl']
    res_bytes = total_bytes['resuser']['lwapp_dl'] + total_bytes['resuser']['behop_dl']
    dyn_bytes = total_bytes['dynuser']['lwapp_dl'] + total_bytes['dynuser']['behop_dl']
    other_bytes = total_bytes['otheruser']['lwapp_dl'] + total_bytes['otheruser']['behop_dl']
    behop_bytes = total_bytes['behopuser']['lwapp_dl'] + total_bytes['behopuser']['behop_dl']
    behop_served_bytes = total_bytes['behopuser']['behop_dl']
    ind = np.arange(1)
    width = 0.35
    bottom = 0
    plt.figure()
    for val,col,label in zip((dyn_bytes,other_bytes,behop_served_bytes,
                              behop_bytes - behop_served_bytes,res_bytes - behop_bytes),
                             ('r','b','g','c','m'),('dyn','other','BeHop (served)','BeHop (lwapp-served)','ResComp (no BeHop)')):
        val = val/2**30
        bar = plt.bar(ind,val,width,color=col,bottom=bottom,label=label)
        bottom = val + bottom
    plt.xlim([0,1])
    plt.ylabel('GB')
    plt.legend()
    plt.xticks([])
    plt.savefig('traffic_breakdown.png')

    plt.figure()
    bottom = 0
    for val,col,label in zip((len(dyn_clients),len(other_clients),len(behop_clients),len(res_clients) - len(behop_clients)),
                             ('r','b','g','c'),('dyn','other','BeHop','ResComp (no BeHop)')):
        val = val
        bar = plt.bar(ind,val,width,color=col,bottom=bottom,label=label)
        bottom = val + bottom
    plt.xlim([0,1])
    plt.ylabel('# of devices')
    plt.legend()
    plt.xticks([])
    plt.savefig('client_breakdown.png')



def analyze_transfers(clients):
    '''Analyze transfers for studio 5 clients.
    Prints (pkts,bytes) for LWAPP-5 and BeHop-5.
    '''
    transfer_logs = TransferLog.objects.filter(timestamp__gt=starting_day,timestamp__lt=final_day,
                                               client__in=clients)
    transfers = {}
    users = {}
    device_type = {}
    total_bytes = {'lwapp_dl':0,'lwapp_ul':0,'behop_dl':0,'behop_ul':0}
    total_packets = {'lwapp_dl':0,'lwapp_ul':0,'behop_dl':0,'behop_ul':0}


    for client in sorted(clients):
        client_transfers = [log for log in transfer_logs if log.client==client]
        lwapp_transfers = [log for log in client_transfers if log.location=='S4']
        behop_transfers = [log for log in client_transfers if log.location=='S5']
        lwapp_dl_pkts = sum([l.in_pkts for l in lwapp_transfers])
        lwapp_ul_pkts = sum([l.out_pkts for l in lwapp_transfers])
        lwapp_dl_bytes = sum([l.in_bytes for l in lwapp_transfers])
        lwapp_ul_bytes = sum([l.out_bytes for l in lwapp_transfers])
        behop_dl_pkts = sum([l.in_pkts for l in behop_transfers])
        behop_ul_pkts = sum([l.out_pkts for l in behop_transfers])
        behop_dl_bytes = sum([l.in_bytes for l in behop_transfers])
        behop_ul_bytes = sum([l.out_bytes for l in behop_transfers])
        total_dl_pkts = lwapp_dl_pkts + behop_dl_pkts
        total_ul_pkts = lwapp_ul_pkts + behop_ul_pkts
        if total_dl_pkts > 0:
            lwapp_dl_pkt_perc = lwapp_dl_pkts/float(total_dl_pkts)
            behop_dl_pkt_perc = behop_dl_pkts/float(total_dl_pkts)
        else:
            lwapp_dl_pkt_perc = 0
            behop_dl_pkt_perc = 0
        if total_ul_pkts > 0:
            lwapp_ul_pkt_perc = lwapp_ul_pkts/float(total_ul_pkts)
            behop_ul_pkt_perc = behop_ul_pkts/float(total_ul_pkts)
        else:
            lwapp_ul_pkt_perc = 0
            behop_ul_pkt_perc = 0

        if client == "none":
            continue
        try:
            username = Client.objects.get(ip_address=client).user
            device_type[client] = Client.objects.get(ip_address=client).type
        except:
            username = client
            device_type[client] = 'undocumented'
        users[client] = username
        transfers[client] = {'lwapp_dl_pkts':lwapp_dl_pkts,'lwapp_ul_pkts':lwapp_ul_pkts,
                             'lwapp_dl_bytes':lwapp_dl_bytes,'lwapp_ul_bytes':lwapp_ul_bytes,
                             'behop_dl_pkts':behop_dl_pkts,'behop_ul_pkts':behop_ul_pkts,                             
                             'behop_dl_bytes':behop_dl_bytes,'behop_ul_bytes':behop_ul_bytes,
                             'total_dl_pkts':total_dl_pkts, 'total_ul_pkts':total_ul_pkts,
                             'behop_dl_pkt_perc':behop_dl_pkt_perc, 'behop_ul_pkt_perc':behop_ul_pkt_perc,
                             'lwapp_dl_pkt_perc':lwapp_dl_pkt_perc,'lwapp_ul_pkt_perc':lwapp_ul_pkt_perc}
        total_bytes['lwapp_dl'] += lwapp_dl_bytes
        total_bytes['lwapp_ul'] += lwapp_ul_bytes
        total_bytes['behop_dl'] += behop_dl_bytes
        total_bytes['behop_ul'] += behop_ul_bytes
        total_packets['lwapp_dl'] += lwapp_dl_pkts
        total_packets['lwapp_ul'] += lwapp_ul_pkts
        total_packets['behop_dl'] += behop_dl_pkts
        total_packets['behop_ul'] += behop_ul_pkts


        
    logging.warning("Index\tClient\t\t\tUser\t\t\tLWAPP-DL-Pkts\tLWAPP-UL-Pkts\tLWAPP-DL-Bytes (MB)\tLWAPP-UL-Bytes (MB)\tBeHop-DL-Pkts\tBeHop-UL-Pkts\tBeHop-DL-Bytes (MB)\tBeHop-UL-Bytes (MB)")
    idx = 0
    for client in sorted(transfers.keys(),key=lambda k:transfers[k]['behop_dl_pkts']):
        idx += 1
        transfer = transfers[client]
        logging.warning("%02d %15s %8s(%14s)\t%10d(%01.2f)\t%10d(%01.2f)\t%7.2f\t\t%7.2f\t\t%10d(%01.2f)\t%10d(%1.2f)\t%7.2f\t\t%7.2f" % 
                        (idx,client, users[client], device_type[client],
                         transfer['lwapp_dl_pkts'],transfer['lwapp_dl_pkt_perc'],
                         transfer['lwapp_ul_pkts'],transfer['lwapp_ul_pkt_perc'],
                         transfer['lwapp_dl_bytes']/float(2**20),transfer['lwapp_ul_bytes']/float(2**20),
                         transfer['behop_dl_pkts'],transfer['behop_dl_pkt_perc'],
                         transfer['behop_ul_pkts'],transfer['behop_ul_pkt_perc'],
                         transfer['behop_dl_bytes']/float(2**20),transfer['behop_ul_bytes']/float(2**20)))

    logging.warning("Total(DL/UL): %1.2fMB|%1.2fMB\tLWAPP(DL/UL): %1.2fMB|%1.2fMB\tBeHop(DL/UL): %1.2fMB|%1.2fMB" % 
                    ((total_bytes['lwapp_dl']+total_bytes['behop_dl'])/float(2**20),(total_bytes['lwapp_ul'] + total_bytes['behop_ul'])/float(2**20),
                     total_bytes['lwapp_dl']/float(2**20),total_bytes['lwapp_ul']/float(2**20),
                     total_bytes['behop_dl']/float(2**20),total_bytes['behop_ul']/float(2**20)))
    return total_bytes


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='BeHop dashboard offline analysis tool.')
    parser.add_argument('--sday', default=None, type=int, nargs='+',help='Starting date (YYYY MM DD)')
    parser.add_argument('--fday', default=None, type=int, nargs='+',help='Final date (YYYY MM DD)')
    parser.add_argument('--os',default=None, type=str, help='Operating System to look for')
    parser.add_argument('--user',default=None,type=str, nargs='+',help="User to look for")
    parser.add_argument('--vuser',default=None,type=str, nargs='+',help="User not to look for")
    parser.add_argument('--loc',default=['S5'],type=str, nargs='+',help="Location to look for")
    parser.add_argument('--alluser', action='store_true',help="Plot results for all heard clients (overrides --user --vuser options)")
    parser.add_argument('--dynuser', action='store_true',help="Plot results for users with IP from the dynamic-ip range")
    parser.add_argument('--resuser', action='store_true',help="Plot results for users with ResComp ip address")
    parser.add_argument('--otheruser', action='store_true',help="Plot results for users from other wireless zones")
    parser.add_argument('--transfer', action='store_true')
    parser.add_argument('--bandwidth', action='store_true')
    parser.add_argument('--netflix', action='store_true')
    parser.add_argument('--youtube', action='store_true')
    parser.add_argument('--breakdown', action='store_true')

    args = parser.parse_args()

    if args.sday:
        sday = args.sday
        if len(sday) == 3:
            sday.append(0)
        starting_day = datetime(sday[0],sday[1],sday[2],sday[3],tzinfo=pytz.timezone('US/Pacific'))
    else:
        starting_day = STARTING_DAY

    if args.fday:
        fday = args.fday
        if len(fday) == 3:
            fday.append(0)
        final_day = datetime(fday[0],fday[1],fday[2],fday[3],tzinfo=pytz.timezone('US/Pacific'))
    else:
        final_day = FINAL_DAY

    if args.os and args.os in OS_ABBRV.keys():
        client_os = [OS_ABBRV[args.os]]
    else:
        client_os = Client.objects.all().values('os').distinct()

    if args.alluser or args.dynuser or args.resuser or args.otheruser:
        db_clients = BandwidthLog.objects.filter(timestamp__gt=starting_day,timestamp__lt=final_day).values('client').distinct()
    elif args.user:
        db_clients = Client.objects.filter(location__in=args.loc,os__in=client_os,user__in=args.user).values('ip_address').distinct()
    elif args.vuser:
        db_clients = Client.objects.filter(location__in=args.loc,os__in=client_os).exclude(user__in=args.vuser).values('ip_address').distinct()
    else:
        db_clients = Client.objects.filter(location__in=args.loc,os__in=client_os).values('ip_address').distinct()

    clients = [cl.values()[0] for cl in db_clients]
    #all_clients = [cl.values()[0] for cl in db_clients]
    #db_clients = Client.objects.filter(location__in=args.loc,os__in=client_os).values('ip_address').distinct()
    #behop_clients =[cl.values()[0] for cl in db_clients]
    #undoc_clients = [ cl for cl in all_clients if cl not in behop_clients]
    #print "\n".join(undoc_clients)

    if args.dynuser:
        clients = [cl for cl in clients if cl.startswith("10.30.8") or cl.startswith("10.30.9")]
    elif args.resuser:
        clients = [cl for cl in clients if cl.startswith("10.30.6") or cl.startswith("10.30.7")]
    elif args.otheruser:
        clients = [cl for cl in clients if not (cl.startswith("10.30.6") or cl.startswith("10.30.7") or cl.startswith("10.30.8") or cl.startswith("10.30.9"))]
    
    if args.transfer:
        analyze_transfers(clients)

    if args.bandwidth:
        analyze_bandwidth(clients)

    if args.netflix:
        analyze_video_bitrate(clients,'netflix')

    if args.youtube:
        analyze_video_bitrate(clients,'youtube')

    if args.breakdown:
        analyze_traffic_breakdown()
