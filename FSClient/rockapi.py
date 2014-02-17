'''
handle jQuery POST requests from the client browser
'''

import webapp2

class RockAPIHandler(webapp2.RequestHandler):

	def post(self, *args, **kwargs):
		import cgi,json
		import fsapi,services,employees

		self.response.headers['Content-Type'] = 'application/json'

		request = cgi.escape(self.request.get('request'))

		if request == u'whooffers':
			selservice = cgi.escape(self.request.get('serviceid'))
			servicesobj = fsapi.apirequest('services')
			servicesobj = servicesobj.content
			servicesobj = json.loads(servicesobj)
			employeelist = services.whooffers(selservice,servicesobj)

			response = employeelist
			print 'WHOOFFERS ', response
		elif request == u'getopenings':
			import openings,datetimemgmt
			selserviceid = cgi.escape(self.request.get('serviceid'))
			selemployeeid = cgi.escape(self.request.get('employeeid'))
			if selemployeeid == 'Any':
				selemployeeid = None
			fsrange = datetimemgmt.getfsrange()
			fsafter = fsrange[0]
			fsbefore = fsrange[1]
			post = {'service' : selserviceid, 'employee' : selemployeeid, 'after' : fsafter, 'before' :fsbefore}
			post = json.dumps(post)
			openingobj = fsapi.apirequest('openings',post)
			openingobj = json.loads(openingobj.content)
			response = openings.gethtml(openingobj)
		else:
			response = "Unknown value for REQUEST"

		self.response.write(response)

application = webapp2.WSGIApplication([
	(r'/api', RockAPIHandler),
], debug=False)