# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Headshot'
        db.create_table('home_headshot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('home', ['Headshot'])

        # Adding model 'Location'
        db.create_table('home_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('street_address_hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city_hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('postalcode', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('home', ['Location'])

        # Adding model 'Presentation'
        db.create_table('home_presentation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('presentation_title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('presentation_length', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('presentation_slides', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('presentation_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('presentation_hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('presentation_thumbmail', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('home', ['Presentation'])

        # Adding model 'UserProfile'
        db.create_table('home_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('languages', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('new_profile', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('home', ['UserProfile'])

        # Adding M2M table for field headshots on 'UserProfile'
        db.create_table('home_userprofile_headshots', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['home.userprofile'], null=False)),
            ('headshot', models.ForeignKey(orm['home.headshot'], null=False))
        ))
        db.create_unique('home_userprofile_headshots', ['userprofile_id', 'headshot_id'])

        # Adding M2M table for field presentations on 'UserProfile'
        db.create_table('home_userprofile_presentations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['home.userprofile'], null=False)),
            ('presentation', models.ForeignKey(orm['home.presentation'], null=False))
        ))
        db.create_unique('home_userprofile_presentations', ['userprofile_id', 'presentation_id'])

        # Adding M2M table for field locations on 'UserProfile'
        db.create_table('home_userprofile_locations', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['home.userprofile'], null=False)),
            ('location', models.ForeignKey(orm['home.location'], null=False))
        ))
        db.create_unique('home_userprofile_locations', ['userprofile_id', 'location_id'])


    def backwards(self, orm):
        # Deleting model 'Headshot'
        db.delete_table('home_headshot')

        # Deleting model 'Location'
        db.delete_table('home_location')

        # Deleting model 'Presentation'
        db.delete_table('home_presentation')

        # Deleting model 'UserProfile'
        db.delete_table('home_userprofile')

        # Removing M2M table for field headshots on 'UserProfile'
        db.delete_table('home_userprofile_headshots')

        # Removing M2M table for field presentations on 'UserProfile'
        db.delete_table('home_userprofile_presentations')

        # Removing M2M table for field locations on 'UserProfile'
        db.delete_table('home_userprofile_locations')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'home.headshot': {
            'Meta': {'object_name': 'Headshot'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'home.location': {
            'Meta': {'object_name': 'Location'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'postalcode': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'street_address_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'home.presentation': {
            'Meta': {'object_name': 'Presentation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'presentation_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'presentation_length': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'presentation_slides': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'presentation_thumbmail': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'presentation_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'presentation_type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'home.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'headshots': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['home.Headshot']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['home.Location']", 'symmetrical': 'False'}),
            'new_profile': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'presentations': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['home.Presentation']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['home']