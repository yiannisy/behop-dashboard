# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'NetflixLog.session_id'
        db.alter_column(u'logs_netflixlog', 'session_id', self.gf('django.db.models.fields.CharField')(max_length=120, null=True))


    def backwards(self, orm):
        
        # Changing field 'NetflixLog.session_id'
        db.alter_column(u'logs_netflixlog', 'session_id', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))


    models = {
        u'logs.client': {
            'Meta': {'object_name': 'Client'},
            'bands_2GHz': ('django.db.models.fields.BooleanField', [], {}),
            'bands_5GHz': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'mac_address': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'})
        },
        u'logs.eventlog': {
            'Meta': {'object_name': 'EventLog'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'client': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'dpid': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'event_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'S5'", 'max_length': '2'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'logs.netflixlog': {
            'Meta': {'object_name': 'NetflixLog'},
            'bits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'client': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'dur': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'S5'", 'max_length': '2'}),
            'rate': ('django.db.models.fields.FloatField', [], {}),
            'session_id': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'logs.rttlog': {
            'Meta': {'object_name': 'RttLog'},
            'client': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'S5'", 'max_length': '2'}),
            'rtt': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'timestamp': ('django.db.models.fields.FloatField', [], {})
        },
        u'logs.transferlog': {
            'Meta': {'object_name': 'TransferLog'},
            'client': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_bytes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'in_pkts': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'S5'", 'max_length': '2'}),
            'out_bytes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'out_pkts': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'logs.youtubelog': {
            'Meta': {'object_name': 'YoutubeLog'},
            'bits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'client': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'dur': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'S5'", 'max_length': '2'}),
            'rate': ('django.db.models.fields.FloatField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['logs']
