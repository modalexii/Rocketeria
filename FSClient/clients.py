def fs_client_from(email):
	'''
	Return the fullSlate client object with an email address matching EMAIL
	if no match is found, None is returned
	if retrieving info on a client fails, None is returned
	'''
	import fsapi
	import json

	# get all valid IDs
	fs_clients = fsapi.apirequest("clients?include=emails,phone_numbers,addresses")
	fs_clients = json.loads(fs_clients.content)
	for c in fs_clients: # each client
		for e in c["emails"]: # each email object
			if e["address"] == email:
				return c # entire FullSlate client object

def fsPack_phones(numbers):
	'''
	NUMBERS is list of phone numbers in any format that FullSlate will accept
	Returns list of dicts in FullSlate's format
	'''
	fs_numbers = []
	for idx, val in enumerate(numbers):
		fs_numbers.append({ "position" : idx + 1, "number" : val })
	return fs_numbers

def fsPack_emails(emails):
	'''
	EMAILS is list of strings that are email addresses
	Returns list of dicts in FullSlate's format
	'''
	fs_emails = []
	for idx, val in enumerate(emails):
		fs_emails.append({ "position" : idx + 1, "address" : val })
	return fs_emails

def fsPack_family_names(holder1_first,holder1_last,holder2_first="",holder2_last="",children=[]):
	'''
	Wrap given names into a first and last name to give to FullSlate
	CHILDREN_FULL is a list if strings representing first OR full names of children 
	All other parameters are strings
	Returns tuple (first_name, last_name)
	Must be passed both first and last name for parent(s)
	'''
	first_name = holder1_first # "Alice"
	if holder2_first: # "Alice & Bob"
		first_name = "%s & %s" % (first_name, holder2_first)
	for c in children: # "Alice & Bob/Don/Sue/Emma..."
		first_name = "%s/%s" % (first_name, c)

	last_name = holder1_last # "Smith"
	try:
		if holder2_last != holder1_last: # "Smith/Jenkins"
			last_name = "%s/%s" % (last_name, holder2_last)
	except NameError:
		pass

	return (first_name,last_name)

def unPack_family_names(names):
	'''
	Opposite (ish) of fsPack_family_names
	NAMES is tuple of first,last as seen by FullSlate
	Returns dict structured like the input params of fsPack_family_names
	'''
	first_name = names[0].split("/")  # "Alice & Bob","Don","Sue","Emma"...
	children = first_name[1:] # "Don","Sue","Emma"..
	parents_firsts = first_name[0].split("&") # "Alice "," Bob"
	holder1_first = parents_firsts[0].strip() # "Alice"
	try:
		holder2_first = parents_firsts[1].strip() # "Bob"
	except IndexError: # no 2nd name
		pass

	last_name = names[1].split("/") # "Smith","Jenkins"
	holder1_last = last_name[0].strip() # "Smith"
	try:
		holder2_last = last_name[1].strip() # "Jenkins"
	except IndexError: # no 2nd name
		pass

	# make non-existant things empty strings while building a dict to return
	unpacked_names = {}
	for n in ["holder1_first","holder1_last","holder2_first","holder2_last","children"]:
		try:
			unpacked_names[n] = eval(n)
		except NameError:
			unpacked_names[n] = ""

	return unpacked_names

class RockClient():

	def __init__(self,fs_client,federated_user):

		self.id = fs_client["id"] # there will always be in ID if the email lookup succeeded
		self.email = federated_user.email() # always user federated email for everything

		try:
			self.first_name = fs_client["first_name"]
		except KeyError:
			print "got no first name"
		try:
			self.last_name = fs_client["last_name"]
		except KeyError:
			print "got no last name"
		try:
			unpacked_names = unPack_family_names(self.first_name,self.last_name)
		except AttributeError: # missing first or last name
			pass
		else:
			self.holder1_first = unpacked_names["holder1_first"]
			self.holder1_last = unpacked_names["holder1_last"]
			self.holder2_first = unpacked_names["holder2_first"]
			self.holder2_last = unpacked_names["holder2_last"]
			self.children = unpacked_names["children"]

		try:
			self.emails = fs_client["emails"]
		except KeyError:
			print "got no emails"
		else:
			# singular primary email, needed for booking
			for e in self.emails:
				if e["position"] == 1:
					self.email = e["address"]
		try:
			self.phone_numbers = fs_client["phone_numbers"]
		except KeyError:
			print "got no phone numbers"
		else:
			# singular primary phone_number, needed for booking
			for n in self.phone_numbers:
				if n["position"] == 1:
					self.phone_number = n["number"]
		try:
			self.addresses = fs_client["addresses"]
		except KeyError:
			print "got no address"
		else:
			# singular primary address, needed for booking
			# addresses is a list of dicts, but dicts have no key "position"
			self.street1 = self.addresses[0]["street1"]
			try:
				self.street2 = self.addresses[0]["street2"]
			except KeyError: # street2 not necessary
				self.street2 = ""
			self.city = self.addresses[0]["city"]
			self.state = self.addresses[0]["state"]
			self.postal_code = self.addresses[0]["postal_code"]
		#try:
		#	self.right_to_contact = fs_client["right_to_contact"]
		#except KeyError:
		#	print "got no right to contact"
		try:
			self.active = fs_client["active"] # nothing is done with this info yet
		except KeyError:
			print "got no active"

	def events_attended(self,fs_range):
		'''
		Get FullSlate event objects attended by SELF
		"TO","AT" & "OCCURRENCE_AT" strings are replaced with datetime objects
		FS_RANGE is dict as returned by ranges.getfsrange()
		Returns list
		'''
		import fsapi,fs_datetime
		import json
		from urllib import urlencode

		start = fs_datetime.fullslateify(fs_range["after"], "%Y%m%d")
		stop = fs_datetime.fullslateify(fs_range["before"], "%Y%m%d")

		all_fs_events = fsapi.apirequest('events?start=%s&stop=%s&occurrences=true' % (start, stop))
		all_fs_events = json.loads(all_fs_events.content)

		#print "\n\nALLEVENTS FROM CLIENTS.FS_EVENTS_ATTENDED(): ",allevents
		my_events = []
		for e in all_fs_events:
			#print "\nE OCC_AT FROM FS_EVENTS_ATTENDED(): ",e['occurrence_at']
			try:
				for a in e[u'attendees']:
					if a[u'id'] == self.id: # if client is attending
						# make fs-style strings into datetime objects
						# these are EST and include "-0500", which is cut
						e['at'] = fs_datetime.normalize(e['at'][:-5], "%Y-%m-%dT%H:%M:%S", current_zone="EST")
						e['to'] = fs_datetime.normalize(e['to'][:-5], "%Y-%m-%dT%H:%M:%S", current_zone="EST")
						e['occurrence_at'] = fs_datetime.normalize(e['occurrence_at'][:-5], "%Y-%m-%dT%H:%M:%S", current_zone="EST")
						my_events.append(e)
			except KeyError: # no attendees
				# careful - can also pass on KeyError caused by typo or non-existant element of e
				pass

		return my_events

	def booking_request(self, post, client_info_source, client_info=True, event_info=True):
		'''
		EVENT_INFO is GAE request object containing post data
		CLIENT_INFO_SOURCE is either "fullslate" or "post" and determines if
		CLIENT_INFO/EVENT_INFO are bool and can be used to create an incomplete
		booking object with elements pertaining only to the event or client.
		the client info in the returned object comes from the FullSlate backend
		or from the post data. Use "post" if client is entering data via the
		web app, otherwise "fullslate" is preferred. 
		Returns a JSON object ready to be passed to FullSlate /bookings
		'''
		import cgi,json

		'''
		Critical info - Throw AttributeError if something is missing
		(catch AttributeError wherever one level up in the call stack)
		'''
		fs_request = {}

		if client_info:
			if client_info_source == "fullslate":
				fs_request.update({
					# from FullSlate
					"first_name" : self.first_name,
					"last_name" : self.last_name,
					"street1" : self.street1,
					"street2" : self.street2,
					"city" : self.city,
					"state" : self.state,
					"postal_code" : self.postal_code,
					"email" : self.email,
					"phone_number" : self.phone_number,
				})
				print '\n\nCLIENTS() INFO_SOURCE = FULLSLATE!'
			elif client_info_source == "post":
				'''
				Used to collect info from clients.
				"Missing" attributes are empty strings and will not throw
				exceptions if used later.
				'''
				"holder1_first" = post.get("holder1_first")
				"holder1_last" = post.get("holder1_last")
				"holder2_first" = post.get("holder2_first")
				"holder2_last" = post.get("holder2_last")
				"children" = post.get("children")
				packed_names = fsPack_family_names(holder1_first,holder1_last,holder2_first,holder2_last,children)
				fs_request.update({
					# from web request
					"first_name" : packed_names[0],
					"last_name" : packed_names[1],
					"street1" : post.get("street1"),
					"street2" : post.get("street2"),
					"city" : post.get("city"),
					"state" : post.get("state"),
					"postal_code" : post.get("postal_code"),
					"email" : self.email, # force use of federated email to avoid security risk
					"phone_number" : post.get("phone_number"),
				})
				print '\n\nCLIENTS() INFO_SOURCE = POST!'

		if event_info:
			# critical info - fail if missing
			fs_request.update({
				# from web request
				"at" : post.get("at"),
				"service" : post.get("service"),
				"employee" : post.get("employee"),
			})
			# non-critical info - ignore if missing
			try:
				fs_request["notes"] = post.get("notes")
			except AttributeError:
				pass
			try:
				fs_request["promo"] = post.get("promo")
			except AttributeError:
				pass
			try:
				fs_request["right_to_contact"] = post.get("right_to_contact")
			except AttributeError:
				pass

		fs_request = json.dumps(fs_request)

		return fs_request
