from django.contrib import admin
from logs.models import *

class NetflixLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp','client','rate')

class YoutubeLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp','client','rate')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'type', 'os', 'user', 'bands_5GHz')

# Register your models here.
admin.site.register(EventLog)
admin.site.register(RttLog)
admin.site.register(NetflixLog, NetflixLogAdmin)
admin.site.register(YoutubeLog, YoutubeLogAdmin)
admin.site.register(Client, ClientAdmin)
