import webapp2

class DevRootHandler(webapp2.RequestHandler):

	def get(self):
		'''handle HTTP GETs'''
		self.response.headers['Content-Type'] = 'text/html'
		import htmlblob
		webcode = htmlblob.get("devroot")
		self.response.write(webcode)

class LessonsHandler(webapp2.RequestHandler):

	def get(self, *args, **kwargs):
		'''handle HTTP GETs'''
		import htmlblob
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
			serviceobj = fsapi.request('services')
			serviceobj = serviceobj.content
			serviceobj = json.loads(serviceobj)
			webcode += services.gethtml(serviceobj)
			# pull & format employees from service object
			employeeobj = fsapi.request('employees')
			employeeobj = employeeobj.content
			employeeobj = json.loads(employeeobj)
			webcode += employees.gethtml(employeeobj)
			#webcode += htmlblob.get("book")
		elif "myaccount" in path:
			webcode += htmlblob.get("myaccount")
		else:
			webcode += htmlblob.get("lessons-main")
		webcode += htmlblob.get("rocketeria-tail")
		self.response.write(webcode) 


class JQReqHandler(webapp2.RequestHandler):

	def post(self, *args, **kwargs):
		import cgi,json
		import fsapi,services,employees

		self.response.headers['Content-Type'] = 'application/json'

		request = cgi.escape(self.request.get('request'))

		if request == u'whooffers':
			selservice = cgi.escape(self.request.get('serviceid'))
			servicesobj = fsapi.request('services')
			servicesobj = servicesobj.content
			servicesobj = json.loads(servicesobj)
			employeelist = services.whooffers(selservice,servicesobj)

			response = employeelist
			print 'WHOOFFERS ', response
		elif request == u'getopenings':
			print "ok!!"
			selserviceid = cgi.escape(self.request.get('serviceid'))
			selemployeeid = cgi.escape(self.request.get('employeeid'))
			if selemployeeid == 'Any':
				selemployeeid = None
			post = {'service' : selserviceid, 'employee' : selemployeeid, 'range' : 'search'}
			post = json.dumps(post)
			openings = fsapi.request('openings',post)
			print post
			print openings.content
			response = openings.content
		else:
			response = "Unknown value for REQUEST"

		self.response.write(response)

application = webapp2.WSGIApplication([
	(r'/', DevRootHandler),
	(r'/lessons', LessonsHandler),
	webapp2.Route(r'/lessons/api', JQReqHandler),
	webapp2.Route(r'/lessons/<:.*>', LessonsHandler),
], debug=False)
