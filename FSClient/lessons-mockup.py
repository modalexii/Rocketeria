import webapp2

class LessonsHandler(webapp2.RequestHandler):

	def get(self, *args, **kwargs):
		'''handle HTTP GETs'''
		import htmlblob
		from google.appengine.api import users
		self.response.headers['Content-Type'] = 'text/html'
		webcode = htmlblob.get("rocketeria-head",)

		try:
			path = args[0]
		except IndexError:
			path = ""
		if "book" in path:
			import fsapi,services,employees
			import json
			# pull services from FS
			serviceobj = fsapi.apirequest('services')

			serviceobj = serviceobj.content
			serviceobj = json.loads(serviceobj)
			
			# pull & format employees from service object
			employeeobj = fsapi.apirequest('employees')
			employeeobj = employeeobj.content
			employeeobj = json.loads(employeeobj)
			

			webcode += htmlblob.get('emptycalendardiv')
			webcode += employees.gethtml(employeeobj)
			webcode += services.gethtml(serviceobj)
			#webcode += htmlblob.get("book")
		elif "loggedout" in path:
			webcode += htmlblob.get("loggedout")
		else:
			webcode += htmlblob.get("lessons-main",)
		webcode += htmlblob.get("rocketeria-tail")
		self.response.write(webcode) 

application = webapp2.WSGIApplication([
	(r'/lessons', LessonsHandler),
	webapp2.Route(r'/lessons/<:.*>', LessonsHandler),
], debug=False)