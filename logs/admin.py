from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from logs.models import *

from datetime import datetime
import time

class EventLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp','client','event_name','event_signal', 'dpid','category','band','location')
    list_filter = ('client','event_name','category','location')
    search_fields = ('client','event_name','category')

class NetflixLogAdmin(admin.ModelAdmin):
    list_display = ('location','timestamp','client','rate','dur','bits', 'session_id')
    list_filter = ('location',)

class NetflixBitrateLogAdmin(admin.ModelAdmin):
    list_display = ('location','timestamp','client','target','bitrate_up','bitrate_down','packetrate_up','packetrate_down')
    list_filter = ('location','client','timestamp')
    search_fields = ('client','location')

class YoutubeLogAdmin(admin.ModelAdmin):
    list_display = ('location','timestamp','client','rate','dur','bits')
    list_filter = ('location',)

class YoutubeBitrateLogAdmin(admin.ModelAdmin):
    list_display = ('location','timestamp','client','target','bitrate_up','bitrate_down','packetrate_up','packetrate_down')
    list_filter = ('location','client')
    search_fields = ('client','location')

class RttLogAdmin(admin.ModelAdmin):
    list_display = ('location','timestamp','client','rtt')
    list_filter = ['client']

class TransferLogAdmin(admin.ModelAdmin):
    list_display = ('location','timestamp','client','in_pkts','out_pkts','in_bytes','out_bytes')
    list_filter = ['client','location','timestamp']


class BandwidthLogAdmin(admin.ModelAdmin):
    list_display = ('location','timestamp','client','in_bytes','out_bytes','in_avgrate_bps','out_avgrate_bps')
    list_filter = ['client','timestamp','location']
    
class WifiIntfLogAdmin(admin.ModelAdmin):
    list_display = ('dpid','timestamp','intf','rx_pkts','rx_bytes',
                    'tx_pkts','tx_bytes')
    search_fields = ('dpid','intf')
    list_filter = ('dpid','timestamp','intf')

class ChannelUtilLogAdmin(admin.ModelAdmin):
    list_display = ('dpid','timestamp','freq','intf','active','busy',
                    'receive','transmit')
    search_fields = ('dpid','intf')
    list_filter = ('dpid','timestamp','intf')
    

class ClientAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'mac_address', 'location','type', 'os', 'user', 'bands_5GHz', 
                    'last_seen','last_heard',
                    'bytes_dl_last','bytes_upl_last','netflix_mins','youtube_mins','bytes_dl','bytes_upl',
                    'rtt_samples','pkts_dl','pkts_upl',)
    list_filter = ('type','bands_5GHz','last_detected','last_seen','last_heard','user',
                   'last_detected','last_detected_5GHz','last_detected_2GHz','location')
    search_fields = ('ip_address','type','os','user','location','mac_address')
    actions = ['show_stats']

    def show_stats(self, request, queryset):
        #response = HttpResponse(content_type="application/json")
        #serializers.serialize("json",queryset, stream=response)
        #return response
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("/logs/stats?clients=%s" % (",".join(selected)))

# Register your models here.
admin.site.register(EventLog,EventLogAdmin)
admin.site.register(RttLog, RttLogAdmin)
admin.site.register(NetflixLog, NetflixLogAdmin)
admin.site.register(NetflixBitrateLog, NetflixBitrateLogAdmin)
admin.site.register(YoutubeLog, YoutubeLogAdmin)
admin.site.register(YoutubeBitrateLog, YoutubeBitrateLogAdmin)
admin.site.register(TransferLog, TransferLogAdmin)
admin.site.register(BandwidthLog, BandwidthLogAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(WifiIntfLog,WifiIntfLogAdmin)
admin.site.register(ChannelUtilLog, ChannelUtilLogAdmin)
