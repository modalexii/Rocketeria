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

		post = {}

		bookings = fsapi.apirequest('bookings',post)

		self.response.write(bookings.content)

		self.response.write('''</body></html>''')

application = webapp2.WSGIApplication([
	(r'/test', TestHandler),
], debug=False)