from django.db import models

# Create your models here.
class EventLog(models.Model):
    timestamp = models.DateTimeField()
    client = models.CharField(max_length=12)
    dpid = models.CharField(max_length=12)
    category= models.CharField(max_length=24)
    event_name = models.CharField(max_length=100)

class RttLog(models.Model):
    timestamp = models.FloatField()
    client = models.IPAddressField()
    rtt = models.PositiveIntegerField()

class NetflixLog(models.Model):
    timestamp = models.DateTimeField()
    client = models.IPAddressField()
    bits = models.PositiveIntegerField()
    dur = models.FloatField()
    rate = models.FloatField()

class YoutubeLog(models.Model):
    timestamp = models.DateTimeField()
    client = models.IPAddressField()
    bits = models.PositiveIntegerField()
    dur = models.FloatField()
    rate = models.FloatField()

class Client(models.Model):
    ip_address = models.IPAddressField()
    mac_address = models.CharField(max_length=12)
    user = models.CharField(max_length=40,null=True)
    type = models.CharField(max_length=40,null=True)
    os = models.CharField(max_length=40,null=True)
    bands_2GHz = models.BooleanField()
    bands_5GHz = models.BooleanField()
    
