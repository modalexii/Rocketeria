from google.appengine.ext import ndb
import logging


class Page(ndb.Model):
    uri = ndb.StringProperty(required = True)
    content = ndb.StringProperty(required = True)

def add_or_update_page(uri, content):
    new_page = Page(id = uri, uri = uri, content = content)
    key = new_page.put()
    return key

def delete_page(uri):
    ndb.Key(Page, uri).delete()

def fetch_content(uri):
    target = Page.get_by_id(uri)
    return target.content
