# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShelfItem'
        db.create_table(u'awesome_shelfitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shelf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['awesome.Shelf'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('unique_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('catalog_id', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('physical_format', self.gf('django.db.models.fields.CharField')(default='book', max_length=50)),
            ('cover_art', self.gf('django.db.models.fields.URLField')(max_length=400, null=True, blank=True)),
            ('sort_order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
        ))
        db.send_create_signal(u'awesome', ['ShelfItem'])

        # Adding M2M table for field classifications on 'ShelfItem'
        db.create_table(u'awesome_shelfitem_classifications', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('shelfitem', models.ForeignKey(orm[u'awesome.shelfitem'], null=False)),
            ('classification', models.ForeignKey(orm[u'awesome.classification'], null=False))
        ))
        db.create_unique(u'awesome_shelfitem_classifications', ['shelfitem_id', 'classification_id'])

        # Adding model 'Shelf'
        db.create_table(u'awesome_shelf', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['awesome.Organization'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=4000)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'awesome', ['Shelf'])

        # Adding unique constraint on 'Shelf', fields ['organization', 'slug']
        db.create_unique(u'awesome_shelf', ['organization_id', 'slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'Shelf', fields ['organization', 'slug']
        db.delete_unique(u'awesome_shelf', ['organization_id', 'slug'])

        # Deleting model 'ShelfItem'
        db.delete_table(u'awesome_shelfitem')

        # Removing M2M table for field classifications on 'ShelfItem'
        db.delete_table('awesome_shelfitem_classifications')

        # Deleting model 'Shelf'
        db.delete_table(u'awesome_shelf')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'awesome.branch': {
            'Meta': {'object_name': 'Branch'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'long': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['awesome.Organization']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'awesome.checkin': {
            'Meta': {'object_name': 'Checkin'},
            'checked_in_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checkins'", 'to': u"orm['awesome.Item']"})
        },
        u'awesome.classification': {
            'Meta': {'object_name': 'Classification'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        u'awesome.item': {
            'Meta': {'object_name': 'Item'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['awesome.Branch']"}),
            'catalog_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'classifications': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['awesome.Classification']", 'symmetrical': 'False'}),
            'cover_art': ('django.db.models.fields.URLField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'latest_checkin': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number_checkins': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'physical_format': ('django.db.models.fields.CharField', [], {'default': "'book'", 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'awesome.organization': {
            'Meta': {'object_name': 'Organization'},
            'about_page_blurb': ('django.db.models.fields.TextField', [], {'default': "'The Awesome Box is a collaboration with the Harvard Library Innovation Lab. It allows the community to see what others have found helpful, entertaining, or mind-blowing.'", 'max_length': '4000'}),
            'catalog_base_url': ('django.db.models.fields.URLField', [], {'max_length': '2000'}),
            'catalog_query': ('django.db.models.fields.CharField', [], {'default': "'isbn'", 'max_length': '100'}),
            'cover_password': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'cover_service': ('django.db.models.fields.CharField', [], {'default': "'notset'", 'max_length': '100'}),
            'cover_user_id': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'logo_link': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'public_email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'public_link': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'service_lookup': ('django.db.models.fields.CharField', [], {'default': "'worldcat'", 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '100'}),
            'twitter_intro': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'twitter_oauth_secret': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'twitter_oauth_token': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'twitter_show_title': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'awesome.shelf': {
            'Meta': {'unique_together': "(('organization', 'slug'),)", 'object_name': 'Shelf'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['awesome.Organization']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        u'awesome.shelfitem': {
            'Meta': {'object_name': 'ShelfItem'},
            'catalog_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'classifications': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['awesome.Classification']", 'symmetrical': 'False'}),
            'cover_art': ('django.db.models.fields.URLField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'physical_format': ('django.db.models.fields.CharField', [], {'default': "'book'", 'max_length': '50'}),
            'shelf': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['awesome.Shelf']"}),
            'sort_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['awesome']