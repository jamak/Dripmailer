# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Email'
        db.create_table('drip_emailer_email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('body', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['drip_emailer.Campaign'], null=True)),
            ('next_email', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['drip_emailer.Email'], unique=True, null=True)),
            ('days_to_wait', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('drip_emailer', ['Email'])

        # Adding model 'Prospect'
        db.create_table('drip_emailer_prospect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('signup_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('responded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('last_email_clicked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('recent_email', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emailLastSeen', to=orm['drip_emailer.Email'])),
            ('recent_email_sent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emailLastSent', to=orm['drip_emailer.Email'])),
        ))
        db.send_create_signal('drip_emailer', ['Prospect'])

        # Adding model 'Campaign'
        db.create_table('drip_emailer_campaign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('first', self.gf('django.db.models.fields.related.ForeignKey')(related_name='first campaign email', to=orm['drip_emailer.Email'])),
        ))
        db.send_create_signal('drip_emailer', ['Campaign'])


    def backwards(self, orm):
        # Deleting model 'Email'
        db.delete_table('drip_emailer_email')

        # Deleting model 'Prospect'
        db.delete_table('drip_emailer_prospect')

        # Deleting model 'Campaign'
        db.delete_table('drip_emailer_campaign')


    models = {
        'drip_emailer.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'first': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first campaign email'", 'to': "orm['drip_emailer.Email']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'drip_emailer.email': {
            'Meta': {'object_name': 'Email'},
            'body': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drip_emailer.Campaign']", 'null': 'True'}),
            'days_to_wait': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'next_email': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['drip_emailer.Email']", 'unique': 'True', 'null': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'drip_emailer.prospect': {
            'Meta': {'object_name': 'Prospect'},
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_email_clicked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recent_email': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emailLastSeen'", 'to': "orm['drip_emailer.Email']"}),
            'recent_email_sent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emailLastSent'", 'to': "orm['drip_emailer.Email']"}),
            'responded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'signup_date': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['drip_emailer']