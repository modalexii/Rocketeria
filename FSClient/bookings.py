class BookingRequest():
DEPRICATED - REMOVE!!!

	def __init__(self):
		pass

	def init_from_post(self,post):
		'''
		Sets attributes given in POST 
		POST is an instance of webapp2.RequestHandler.post()
		(typically rockapi.post())
		Non-esistant attributes will be empty strings
		'''
		import cgi

		self.at = cgi.escape(post.get('at'))
		self.service = cgi.escape(post.get('service'))
		self.employee = cgi.escape(post.get('employee'))
		self.notes = cgi.escape(post.get('notes'))
		self.promo = cgi.escape(post.get('promo'))
		self.right_to_contact = cgi.escape(post.get('right_to_contact'))

		if post.get('first_name') or post.get('last_name'): # assume we have both
			self.first_name = post.get('first_name')
			self.first_name = post.get('last_name')
		elif post.get('holder1_first'):
			self.holder1_first = cgi.escape(post.get('holder1_first'))
			self.holder1_last = cgi.escape(post.get('holder1_last'))
			self.holder2_first = cgi.escape(post.get('holder2_first'))
			self.holder2_last = cgi.escape(post.get('holder2_last'))
			try:
				for c in cgi.escape(post.get('children')):
					try:
						self.children.append(cgi.escape(c))
					except NameError: # first entry
						self.children = [cgi.escape(c)]
			except AttributeError: # no "children" in POST
				children = []

			import clients
			names = clients.fsPack_family_names(holder1_first,holder1_last,
												holder2_first,holder2_last,
												children)
			self.first_name = names[0]
			self.last_name = names[1]
		else:
			print "\n\nNO FIRST/LAST_NAME OR HOLDER1_FIRST/LAST PASSED TO bookings.init_from_post! Booking will fail."

	def dump(self):
		'''
		return a JSON object ready to be passed to FullSlate
		'''
		import json
		fs_request = {
			"at" : self.at,
			"service" : self.service,
			"employee" : self.employee,
			"first_name" : self.first_name,
			"last_name" : self.last_name,
			"street1" self.street1,
			"street2" : self.street2,
			"city" : self.city,
			"state" : self.state,
			"postal_code" : self.postal_code,
			"email" : self.email,
			"phone_number" : self.phone_number,
			"notes" : self.notes,
			"promo" : self.promo,
			"right_to_contact" : self.right_to_contact,
		}
		fs_request = json.dumps(fs_request)
		return fs_request