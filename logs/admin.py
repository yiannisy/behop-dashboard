from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from logs.models import *


class NetflixLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp','client','rate')

class YoutubeLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp','client','rate')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'type', 'os', 'user', 'bands_5GHz')
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
admin.site.register(EventLog)
admin.site.register(RttLog)
admin.site.register(NetflixLog, NetflixLogAdmin)
admin.site.register(YoutubeLog, YoutubeLogAdmin)
admin.site.register(Client, ClientAdmin)
