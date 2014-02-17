'''split in to lessons-mockup, rockapi, etc. should be removed!'''

class TestHandler(webapp2.RequestHandler):

	def get(self, *args, **kwargs):
		'''handle HTTP GETs'''
		self.response.headers['Content-Type'] = 'text/html'
		from google.appengine.api import users
		import htmlblob
		webcode = htmlblob.get("rocketeria-head",)
		webcode += htmlblob.get("openid-auth")
		webcode += htmlblob.get("rocketeria-tail")
		self.response.write(webcode) 

application = webapp2.WSGIApplication([
	(r'/', DevRootHandler),
	(r'/lessons', LessonsHandler),
	webapp2.Route(r'/lessons/api', JQReqHandler),
	webapp2.Route(r'/lessons/<:.*>', LessonsHandler),
	(r'/test', TestHandler),
], debug=False)
