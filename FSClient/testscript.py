import webapp2

class TestHandler(webapp2.RequestHandler):

	def get(self):
		'''handle HTTP GETs'''
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write('''<hmtl><body>''')
		import fsapi,json,pprint,clients,rockapi
		
		from pytz.gae import pytz
		from datetime import datetime
		def convert(dte, fromZone, toZone):
			fromZone, toZone = pytz.timezone(fromZone), pytz.timezone(toZone)
			return fromZone.localize(dte, is_dst=True).astimezone(toZone)


		fstime = "20140312T105922Z"  
		dto = datetime.strptime(fstime,"%Y%m%dT%H%M%SZ")

		conv_dto = convert(dto,"America/New_York","GMT",)
		self.response.write("%s, %s" % (dto,conv_dto))

		self.response.write('''</body></html>''')

application = webapp2.WSGIApplication([
	(r'/test', TestHandler),
], debug=False)