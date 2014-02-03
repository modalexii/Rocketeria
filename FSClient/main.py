import webapp2

class DevRootHandler(webapp2.RequestHandler):

	def get(self):
		'''handle HTTP GETs'''
		self.response.headers['Content-Type'] = 'text/html'
		import templates
		webcode = templates.get("devroot")
		self.response.write(webcode)

class LessonsHandler(webapp2.RequestHandler):

	def get(self, *args, **kwargs):
		'''handle HTTP GETs'''
		self.response.headers['Content-Type'] = 'text/html'
		import templates
		webcode = templates.get("rocketeria-head")
		try:
			path = args[0]
		except IndexError:
			path = ""
		if "book" in path:
			webcode += templates.get("book")
		elif "myaccount" in path:
			webcode += templates.get("myaccount")
		else:
			webcode += templates.get("lessons-main")
		webcode += templates.get("rocketeria-tail")
		self.response.write(webcode)

application = webapp2.WSGIApplication([
	(r'/', DevRootHandler),
	(r'/lessons', LessonsHandler),
	webapp2.Route(r'/lessons/<:.*>', LessonsHandler),
], debug=True)
