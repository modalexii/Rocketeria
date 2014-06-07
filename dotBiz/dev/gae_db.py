from google.appengine.ext import ndb
#import logging


class Page(ndb.Model):
	uri = ndb.StringProperty(required = True)
	content = ndb.GenericProperty(indexed = False, required = True)

def add_or_update_page(uri, content):
	new_page = Page(
		id = uri.encode('utf-8', 'xmlcharrefreplace'), 
		uri = uri.encode('utf-8', 'xmlcharrefreplace'), 
		content = content.encode('utf-8', 'xmlcharrefreplace')
	)
	key = new_page.put()
	return key

def delete_page(uri):
	ndb.Key(Page, uri).delete()

def fetch_content(uri):
	#logging.info("DATAFASE FETCH: " + uri)
	target = Page.get_by_id(uri)
	return target.content
