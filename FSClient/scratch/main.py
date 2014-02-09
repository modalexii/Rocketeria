
'''
servicesobj = fsapi.request('services')

print services.gethtml(servicesobj)

myservice = raw_input('Which Service? ')

aplicemployees = services.whooffers(myservice, servicesobj)

print employees.gethtml(aplicemployees)

myemployee = raw_input('Which Employee? ')
'''

import webapp2, fsapi, json
import fsapi, services, employees

class DevTestRootHandler(webapp2.RequestHandler):
	def get(self):
		#post = json.dumps({'service' : '1', 'employee' : '2', })
		webcode = '''<html><body><form>'''
		servicesobj = fsapi.request('services')
		servicesobj = servicesobj.content
		servicesobj = json.loads(servicesobj)
		webcode += services.gethtml(servicesobj)
		myservice = 'Guitar'
		employeelist = services.whooffers(myservice, servicesobj)
		webcode += employees.gethtml(employeelist)
		self.response.write(webcode)

application = webapp2.WSGIApplication([
	(r'/', DevTestRootHandler),
], debug=True)