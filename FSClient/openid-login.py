import webapp2
from google.appengine.api import users

class LoginHandler(webapp2.RequestHandler):

	def get(self):
		continue_url = self.request.GET.get('continue')
		#openid_url = self.request.GET.get('openid')
		self.response.out.write('<html><body>%s</body></html>' % continue_url)

application = webapp2.WSGIApplication([
	(r'/_ah/login', LoginHandler),
], debug=False)