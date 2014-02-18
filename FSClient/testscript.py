'''
render the development server root page...
static html with links to various things
'''

import webapp2

class TestHandler(webapp2.RequestHandler):

	def get(self):
		'''handle HTTP GETs'''
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('''<hmtl><body>''')
		import fsapi,json,pprint,clients

		client = clients.fs_client_from('kylec.steely@gmail.com')
		self.response.write('''<h2>CLIENT OBJECT:</h2>''')
		self.response.write(client)

		allevents = clients.fs_events_attended(id=client['id'],start='2014-03-16',stop='2014-04-10')
		self.response.write('''<h2>EVENT OBJECT:</h2>''')
		self.response.write(allevents)

		self.response.write('''</body></html>''')

application = webapp2.WSGIApplication([
	(r'/test', TestHandler),
], debug=False)