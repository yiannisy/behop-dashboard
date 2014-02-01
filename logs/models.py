from django.db import models

LOC_CHOICES = (
    ('S6', 'LWAPP 6'),
    ('S5', 'Studio 5'),
    ('S4', 'LWAPP 5')
)

# Create your models here.
class EventLog(models.Model):
    location = models.CharField(max_length=2,
                                choices=LOC_CHOICES,
                                default='S5')
    timestamp = models.DateTimeField()
    client = models.CharField(max_length=12)
    dpid = models.CharField(max_length=12, blank=True,default='')
    category= models.CharField(max_length=24,default='WiFi')
    event_name = models.CharField(max_length=100)
    event_signal = models.CharField(max_length=100,blank=True,default='')
    band = models.CharField(max_length=10, default='unknown')

class RttLog(models.Model):
    location = models.CharField(max_length=2,
                                choices=LOC_CHOICES,
                                default='S5')
    timestamp = models.FloatField()
    client = models.IPAddressField()
    rtt = models.PositiveIntegerField()

class NetflixLog(models.Model):
    location = models.CharField(max_length=2,
                                choices=LOC_CHOICES,
                                default='S5')
    timestamp = models.DateTimeField()
    client = models.IPAddressField()
    session_id = models.CharField(max_length=120,null=True)
    bits = models.PositiveIntegerField()
    dur = models.FloatField()
    rate = models.FloatField()

class YoutubeLog(models.Model):
    location = models.CharField(max_length=2,
                                choices=LOC_CHOICES,
                                default='S5')
    timestamp = models.DateTimeField()
    client = models.IPAddressField()
    bits = models.PositiveIntegerField()
    dur = models.FloatField()
    rate = models.FloatField()

class TransferLog(models.Model):
    location = models.CharField(max_length=2,
                                choices=LOC_CHOICES,
                                default='S5')
    timestamp = models.DateTimeField()
    client = models.IPAddressField()
    in_pkts = models.PositiveIntegerField()
    out_pkts = models.PositiveIntegerField()
    in_bytes = models.PositiveIntegerField()
    out_bytes = models.PositiveIntegerField()

class BandwidthLog(models.Model):
    location = models.CharField(max_length=2,
                                choices=LOC_CHOICES,
                                default='S5')
    timestamp = models.DateTimeField()
    client = models.IPAddressField()
    in_bytes = models.PositiveIntegerField()
    out_bytes = models.PositiveIntegerField()
    in_avgrate_bps = models.FloatField()
    out_avgrate_bps = models.FloatField()


class Client(models.Model):
    location = models.CharField(max_length=2,
                                choices=LOC_CHOICES,
                                default='S5')
    ip_address = models.IPAddressField()
    mac_address = models.CharField(max_length=12,unique=True)
    user = models.CharField(max_length=40,null=True)
    type = models.CharField(max_length=40,null=True)
    os = models.CharField(max_length=40,null=True)
    bands_2GHz = models.BooleanField()
    bands_5GHz = models.BooleanField()
    last_seen = models.DateTimeField(blank=True,null=True, verbose_name='Last Served')
    last_heard = models.DateTimeField(blank=True,null=True, verbose_name='Last Attempted')
    last_detected = models.DateTimeField(blank=True, null=True, verbose_name='Last Detected')
    last_detected_5GHz = models.DateTimeField(blank=True, null=True, verbose_name='Last Detected (5GHz)')
    last_detected_2GHz = models.DateTimeField(blank=True, null=True, verbose_name='Last Detected (2GHz)')    
    netflix_mins = models.FloatField(default=0)
    youtube_mins = models.FloatField(default=0)
    rtt_samples = models.PositiveIntegerField(default=0)
    pkts_dl = models.PositiveIntegerField(default=0, verbose_name='DL (pkts)')
    pkts_upl = models.PositiveIntegerField(default=0, verbose_name='UPL (pkts)')
    bytes_dl = models.PositiveIntegerField(default=0,verbose_name='DL (MB)')
    bytes_upl = models.PositiveIntegerField(default=0, verbose_name='UPL (MB)')
    bytes_dl_last = models.PositiveIntegerField(default=0,verbose_name='Usage (DL-MB)')
    bytes_upl_last = models.PositiveIntegerField(default=0, verbose_name='Usage (UPL-MB)')

    
