'''
render the development server root page...
static html with links to various things
'''

import webapp2

class DevRootHandler(webapp2.RequestHandler):

	def get(self):
		'''handle HTTP GETs'''
		import templates
		self.response.headers['Content-Type'] = 'text/html'
		webcode = templates.get("devroot")
		self.response.write(webcode)

application = webapp2.WSGIApplication([
	(r'/', DevRootHandler),
], debug=False)