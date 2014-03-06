'''
handle jQuery POST requests from the client browser
'''

import webapp2

class RockAPIHandler(webapp2.RequestHandler):

	def post(self, *args, **kwargs):
		import cgi,json
		import fsapi,services,employees,events

		request = self.request.get('request') # <<<<< no input sanitizing; fix before pilot PIM!

		if request == u'whooffers':
			self.response.headers['Content-Type'] = 'application/json'

			selservice = cgi.escape(self.request.get('serviceid'))
			servicesobj = fsapi.apirequest('services')
			servicesobj = servicesobj.content
			servicesobj = json.loads(servicesobj)
			employeelist = services.whooffers(selservice,servicesobj)

			response = employeelist
			print 'WHOOFFERS ', response
		elif request == u'getopenings':
			import openings,ranges,fs_datetime

			self.response.headers['Content-Type'] = 'text/html'

			selserviceid = cgi.escape(self.request.get('serviceid'))
			selemployeeid = cgi.escape(self.request.get('employeeid'))

			if selemployeeid == 'Any':
				selemployeeid = None

			fsrange = ranges.getfsrange(offset=0,num_weeks=3)
			fsafter = fs_datetime.fullslateify(fsrange["after"], "%Y%m%dT000000Z")
			fsbefore = fs_datetime.fullslateify(fsrange["before"], "%Y%m%dT115959Z")

			post = {'service' : selserviceid, 'employee' : selemployeeid, 'after' : fsafter, 'before' : fsbefore}
			post = json.dumps(post)

			fs_openings = fsapi.apirequest('openings',post)
			fs_openings = json.loads(fs_openings.content)

			rock_openings = []
			for o in fs_openings["openings"]:
				# make datetime opject for openings.py, and convert to EST
				rock_openings.append(fs_datetime.normalize(o,"%Y%m%dT%H%M%SZ","GMT","EST"))

			#print "ROCKOPENINGS  FROM ROCKAPI: ",rock_openings
			response = events.makecal(rock_openings,3,"new")
		elif request == u"client_form":
			'''
			'''
			from google.appengine.api import users
			import json

			self.response.headers['Content-Type'] = 'text/html'

			federated_user = users.get_current_user()
			if not federated_user: # client-side tampering
				self.error(403)

			#print '\nUSER FROM ROCKAPI: ',federated_user

			import clients,htmlblob
			fs_client = clients.fs_client_from(federated_user.email())
			rock_client = clients.RockClient(fs_client,federated_user)
			data = rock_client # pass the client object to pre-fill form fields

			webcode = htmlblob.get("client_info_form",data)

			response = webcode
		elif request == 'book':
			'''
			Confirm logged in, confirm we have all necessary info, 
			then book an appointment with FullSlate
			'''
			from google.appengine.api import users
			import fsapi,clients,htmlblob

			federated_user = users.get_current_user()

			if not federated_user: # not logged in - display login
				self.response.write(htmlblob.get("federated_login"))
				return
			
			fs_client = clients.fs_client_from(federated_user.email())
			rock_client = clients.RockClient(fs_client,federated_user)

			try:
				print 'TRYING INFO_SOURCE = FULLSLATE (ROCKAPI)'
				post = rock_client.booking_request(self.request, "fullslate") # try to fill out the request w/ info from FullSlate
				print 'INFO_SOURCE = FULLSLATE WORKED! POST LOOKS LIKE THIS: ',post
			except AttributeError as e: # important info missing
				print 'INFO_SOURCE = FULLSLATE FAILED, TRYING INFO_SOURCE = POST (ROCKAPI)', e
				post = rock_client.booking_request(self.request, "post") # try to fill out the request w/ info from POST data

				# let it go through, missing info or not, and let FullSlate return error to client
				print 'POST NOW LOOKS LIKE THIS: ',post,'\nLETTING IT GO TO FULLSLATE...'
				response = fsapi.apirequest('bookings',post)
				if response.status_code != 200:
					print 'FULLSLATE DIDNT LIKE THE BOOKING REQUEST: ',response.status_code,' ',response.content
					print 'SENDING CLIENT INFO FORM...'
					self.response.write(htmlblob.get("client_info_form",rock_client))
					return
					print "\n SHOULD NOT GET HERE! RETURN FAILED...\n"
			finally:
				print 'FINALLY, POST LOOKS LIKE THIS: ',post,'\nLETTING IT GO TO FULLSLATE...'
				response = fsapi.apirequest('bookings',post) # change to redirect to pay/conf/thx
				print '\nFULLSLATE RETURNED THE FOLLOWING BOOKING OBJECT: ',response.content

		else:
			response = "Unknown value for REQUEST"

		#print "\nRESPONSE FROM ROCKAPI: ",response
		self.response.write(response)

application = webapp2.WSGIApplication([
	(r'/api', RockAPIHandler),
], debug=False)