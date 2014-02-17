'''
render the development server root page...
static html with links to various things
'''

import webapp2

class TestHandler(webapp2.RequestHandler):

	def get(self):
		'''handle HTTP GETs'''
		self.response.headers['Content-Type'] = 'text/html'
		webcode = '''<hmtl><body>'''
		import fsapi,json,pprint
		clientobj = fsapi.apirequest('clients')
		clientobj = json.loads(clientobj.content)
		pprint.pprint(clientobj)


		webcode += '''</body></html>'''
		self.response.write(webcode)

application = webapp2.WSGIApplication([
	(r'/test', TestHandler),
], debug=False)