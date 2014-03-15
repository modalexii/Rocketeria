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

			self.response.write(employeelist)

		elif request == u'getopenings':
			import openings,ranges,fs_datetime

			self.response.headers['Content-Type'] = 'text/html'

			selserviceid = cgi.escape(self.request.get('serviceid'))
			selemployeeid = cgi.escape(self.request.get('employeeid'))

			fsrange = ranges.getfsrange(offset=0,num_weeks=3)
			fsafter = fs_datetime.fullslateify(fsrange["after"], "%Y%m%dT000000Z")
			fsbefore = fs_datetime.fullslateify(fsrange["before"], "%Y%m%dT115959Z")

			post = {'service' : selserviceid, 'after' : fsafter, 'before' : fsbefore}
			if selemployeeid != "Any":
				post.update({"employee" : selemployeeid})

			post = json.dumps(post)
			#print "POST DESTINED FOR FULLSLATE API FROM ROCKAPI GETOPENINGS REQUEST: ",post

			fs_openings = fsapi.apirequest('openings',post)
			fs_openings = json.loads(fs_openings.content)
			#print "\nFS_OPENINGS FROM ROCKAPI GETOPENINGS REQUEST: ",fs_openings

			rock_openings = []
			for o in fs_openings["openings"]:
				# make datetime opject for openings.py, and convert to EST
				rock_openings.append(fs_datetime.normalize(o,"%Y%m%dT%H%M%SZ","GMT","America/New_York"))

			#print "ROCKOPENINGS  FROM ROCKAPI: ",rock_openings
			self.response.write(events.makecal(rock_openings,3,"new"))
		elif request == u"client_form":
			'''
			er, is this used by anything?
			me thinks this can be removed...
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

			webcode = rock_client.prefilled_form() #htmlblob.get("client_info_form",data)

			self.response.write(webcode)
		elif request == 'book':
			'''
			Confirm we have all necessary info, 
			then book an appointment with FullSlate

			User must be logged in or else stuff will just break 
			when Book Now is clicked. In future milestones, we can 
			allow anonymous schedule checking
			'''
			from google.appengine.api import users
			import fsapi,clients,htmlblob

			# headers set below as we figure out what exactly we're returning

			federated_user = users.get_current_user()
			
			try:
				fs_client = clients.fs_client_from(federated_user.email())
			except AttributeError as e: 
				# no email - not logged in
				# indicates tampering
				self.error(401) # not really proper http spec but
				self.response.write("401 - No Federated User. Possible client tampering.")
				return
			else:	
				rock_client = clients.RockClient(fs_client,federated_user)

			try:
				print 'TRYING INFO_SOURCE = FULLSLATE (ROCKAPI)'
				post = rock_client.booking_request(self.request, "fullslate") # try to fill out the request w/ info from FullSlate
				print 'INFO_SOURCE = FULLSLATE WORKED! POST LOOKS LIKE THIS: ',post
			except AttributeError as e: # important info missing
				print 'INFO_SOURCE = FULLSLATE FAILED, TRYING INFO_SOURCE = POST (ROCKAPI)', e
				post = rock_client.booking_request(self.request, "post") # try to fill out the request w/ info from POST data

				# let it go through, missing info or not, and let FullSlate return error to client
				booking_response = fsapi.apirequest('bookings',post)
				if booking_response.status_code != 200: 
					print 'FULLSLATE DIDNT LIKE THE BOOKING REQUEST: ',booking_response.status_code,' ',booking_response.content
					print 'SENDING CLIENT INFO FORM...'
					self.response.headers['Content-Type'] = 'text/html'
					self.response.write(rock_client.prefilled_form())
					return
			else:
				print 'FINALLY, POST LOOKS LIKE THIS: ',post,'\nLETTING IT GO TO FULLSLATE...'
				booking_response = fsapi.apirequest('bookings',post)
				print "\nBOOKING RESPONSE: ",booking_response.status_code,booking_response.content
				self.response.headers['Content-Type'] = 'application/json'
				self.response.write(json.dumps({"status_code" : booking_response.status_code, "content" : booking_response.content}))

		elif request == 'cancel':
			'''
			Cancel a booking.
			Expects {"id" : <id>, "at" : <fsat>}
			'''
			import json
			import fsapi

			booking_id = self.request.get('id')
			fs_at = self.request.get('at')

			url = "events/%s" % booking_id
			post = {"at" : fs_at}
			post = json.dumps(post)

			response_to_cancel = fsapi.apirequest(url,post,"delete")
			print "\nRESPONSE_TO_CANCEL: ",response_to_cancel.status_code," ",response_to_cancel.content
			return

		else:
			response = "Unknown value for REQUEST"

application = webapp2.WSGIApplication([
	(r'/api', RockAPIHandler),
], debug=False)