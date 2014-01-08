from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from logs.models import *

from datetime import datetime
import time

class EventLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp','client','event_name','signal')
    list_filter = ('client','event_name')
    search_fields = ('client','event_name')

class NetflixLogAdmin(admin.ModelAdmin):
    list_display = ('location','timestamp','client','rate','dur','bits', 'session_id')

class YoutubeLogAdmin(admin.ModelAdmin):
    list_display = ('location','timestamp','client','rate','dur','bits')

class RttLogAdmin(admin.ModelAdmin):
    list_display = ('location','timestamp','client','rtt')
    list_filter = ['client']

class TransferLogAdmin(admin.ModelAdmin):
    list_display = ('location','timestamp','client','in_pkts','out_pkts','in_bytes','out_bytes')
    list_filter = ['client']

class ClientAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'mac_address', 'type', 'os', 'user', 'bands_5GHz', 'last_seen', 
                    'bytes_dl','bytes_upl','netflix_mins','youtube_mins',
                    'rtt_samples','pkts_dl','pkts_upl',)
    list_filter = ('type','bands_5GHz')
    search_fields = ('type','os','user')
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
admin.site.register(YoutubeLog, YoutubeLogAdmin)
admin.site.register(TransferLog, TransferLogAdmin)
admin.site.register(Client, ClientAdmin)
