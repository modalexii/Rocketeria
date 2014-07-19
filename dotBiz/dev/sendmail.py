import webapp2, logging
from google.appengine.api import mail
import get_env

logging.getLogger().setLevel(logging.INFO)

def templatify(message, remote_addr, remote_ua):
	version = get_env.version()
	environment = get_env.as_hardcoded()
	universal_footer = '''

...
This message was generated by SCMS in response to a form submission on rocketeria.biz.
Please do not reply. The robot cannot hear you scream.

If you believe this message was sent in error or contains an error, please forward it to kyle@rocketeria.biz. Include a brief explaination of the issue.

Environment: {environment}
App Version: {version}
Namespace: sendmail.MailHandler().post()
Client: {remote_addr} via {remote_ua}
	'''

	message.sender = "SCMS Application Server <info@rocketeria.biz>"
	message.to = "kyle@rocketeria.biz"
	message.subject = "[SCMS] %s" % message.subject
	message.body = "%s\n%s" % (message.body, universal_footer)
	message.body = message.body.format(**locals())

	return message


class MailHandler(webapp2.RequestHandler):

	def post(self):

		uri = self.request.path.strip('/')
		message = mail.EmailMessage()

		if uri == "sendmail/deadlink" and badurl:
			badurl = self.request.get("baddurl").encode('utf-8', 'xmlcharrefreplace')
			message.subject = "Missing resource reported by user"
			message.body = '''
A helpful user reported a missing page or file on rocketeria.biz. They were expecting to find something at:

{badurl}

...but got the 404 page instead.
			'''.format(**locals())

		elif uri == "sendmail/changerequest":

			# performs rudimentary checks before sending mail. will not catch but the most basic weirdness.
			account_name = self.request.get("account_name").encode('utf-8', 'xmlcharrefreplace')
			student_name = self.request.get("student_name").encode('utf-8', 'xmlcharrefreplace')

			if account_name and student_name:

				message.subject = "Lesson Change Request for %s" % (student_name)

				lesson_date = self.request.get("lesson_date").encode('utf-8', 'xmlcharrefreplace')
				lesson_time = self.request.get("lesson_time").encode('utf-8', 'xmlcharrefreplace')

				if lesson_date or lesson_time:
					# still send the message if either date or time was missed
			
					message.body = '''
Billing / Account Name: {account_name}

Student {student_name} will not be able to attend the lesson currently scheduled for {lesson_date} at {lesson_time}.

					'''.format(**locals())
	
				else:
					requested_action = self.request.get("requested_action").encode('utf-8', 'xmlcharrefreplace')
					pref_contact = self.request.get("pref_contact").encode('utf-8', 'xmlcharrefreplace')

					if requested_action and pref_contact:
						message.body = '''
Billing / Account Name: {account_name}

Student {student_name} wishes to {requested_action} going forward. Please contact via {pref_contact}.
						'''
			
		try:
			message = templatify(message = message, remote_addr = self.request.remote_addr, remote_ua = self.request.headers['User-Agent'])
		except AttributeError:
			self.error(400)
		else:
			message.send()
		
		self.redirect("/") # just for noscript


application = webapp2.WSGIApplication([
	(r'/sendmail/.*', MailHandler),
], debug=False)


