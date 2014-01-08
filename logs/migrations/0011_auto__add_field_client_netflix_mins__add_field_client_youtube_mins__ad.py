# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Client.netflix_mins'
        db.add_column(u'logs_client', 'netflix_mins', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Adding field 'Client.youtube_mins'
        db.add_column(u'logs_client', 'youtube_mins', self.gf('django.db.models.fields.FloatField')(default=0), keep_default=False)

        # Adding field 'Client.rtt_samples'
        db.add_column(u'logs_client', 'rtt_samples', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'Client.pkts_dl'
        db.add_column(u'logs_client', 'pkts_dl', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'Client.pkts_upl'
        db.add_column(u'logs_client', 'pkts_upl', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'Client.bytes_dl'
        db.add_column(u'logs_client', 'bytes_dl', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'Client.bytes_upl'
        db.add_column(u'logs_client', 'bytes_upl', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Client.netflix_mins'
        db.delete_column(u'logs_client', 'netflix_mins')

        # Deleting field 'Client.youtube_mins'
        db.delete_column(u'logs_client', 'youtube_mins')

        # Deleting field 'Client.rtt_samples'
        db.delete_column(u'logs_client', 'rtt_samples')

        # Deleting field 'Client.pkts_dl'
        db.delete_column(u'logs_client', 'pkts_dl')

        # Deleting field 'Client.pkts_upl'
        db.delete_column(u'logs_client', 'pkts_upl')

        # Deleting field 'Client.bytes_dl'
        db.delete_column(u'logs_client', 'bytes_dl')

        # Deleting field 'Client.bytes_upl'
        db.delete_column(u'logs_client', 'bytes_upl')


    models = {
        u'logs.client': {
            'Meta': {'object_name': 'Client'},
            'bands_2GHz': ('django.db.models.fields.BooleanField', [], {}),
            'bands_5GHz': ('django.db.models.fields.BooleanField', [], {}),
            'bytes_dl': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bytes_upl': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'mac_address': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'netflix_mins': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'pkts_dl': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pkts_upl': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'rtt_samples': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'youtube_mins': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'logs.eventlog': {
            'Meta': {'object_name': 'EventLog'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'WiFi'", 'max_length': '24'}),
            'client': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'dpid': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'event_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "'S5'", 'max_length': '2'}),
            'signal': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
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
