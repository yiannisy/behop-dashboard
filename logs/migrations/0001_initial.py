# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'EventLog'
        db.create_table(u'logs_eventlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('client', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('dpid', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('event_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'logs', ['EventLog'])

        # Adding model 'RttLog'
        db.create_table(u'logs_rttlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('client', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('rtt', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'logs', ['RttLog'])

        # Adding model 'NetflixLog'
        db.create_table(u'logs_netflixlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('client', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('bits', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('dur', self.gf('django.db.models.fields.FloatField')()),
            ('rate', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'logs', ['NetflixLog'])

        # Adding model 'YoutubeLog'
        db.create_table(u'logs_youtubelog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('client', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('bits', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('dur', self.gf('django.db.models.fields.FloatField')()),
            ('rate', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'logs', ['YoutubeLog'])

        # Adding model 'Client'
        db.create_table(u'logs_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('mac_address', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('bands_2GHz', self.gf('django.db.models.fields.BooleanField')()),
            ('bands_5GHz', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'logs', ['Client'])


    def backwards(self, orm):
        
        # Deleting model 'EventLog'
        db.delete_table(u'logs_eventlog')

        # Deleting model 'RttLog'
        db.delete_table(u'logs_rttlog')

        # Deleting model 'NetflixLog'
        db.delete_table(u'logs_netflixlog')

        # Deleting model 'YoutubeLog'
        db.delete_table(u'logs_youtubelog')

        # Deleting model 'Client'
        db.delete_table(u'logs_client')


    models = {
        u'logs.client': {
            'Meta': {'object_name': 'Client'},
            'bands_2GHz': ('django.db.models.fields.BooleanField', [], {}),
            'bands_5GHz': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'mac_address': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        u'logs.eventlog': {
            'Meta': {'object_name': 'EventLog'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'client': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'dpid': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'event_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'logs.netflixlog': {
            'Meta': {'object_name': 'NetflixLog'},
            'bits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'client': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'dur': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.FloatField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'logs.rttlog': {
            'Meta': {'object_name': 'RttLog'},
            'client': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rtt': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'logs.youtubelog': {
            'Meta': {'object_name': 'YoutubeLog'},
            'bits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'client': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'dur': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.FloatField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['logs']
