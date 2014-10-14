import webapp2
from google.appengine.api import mail
import get_env, templates

def templatify_internal(message, remote_addr, remote_ua):
	version = get_env.version()
	environment = get_env.as_hardcoded()

	message.sender = "SCMS Application Server <info@rocketeria.biz>"
	message.to = "info@rocketeria.biz"
	message.subject = "[SCMS] %s" % message.subject

	content = message.body
	full_body = templates.get("mail_template_internal","txt","email").format(**locals())
	message.body = full_body

	return message

def templatify_external(message):

	message.sender = "Rocketeria <info@rocketeria.biz>"
	message.subject = "%s [Automatically Generated]" % message.subject

	content = message.body
	full_body = templates.get("mail_template_external","txt","email").format(**locals())
	message.body = full_body

	return message

class MailHandler(webapp2.RequestHandler):

	def post(self):

		# status is bad until set good
		self.response.set_status(400)

		uri = self.request.path.strip('/')
		messages = {
			"internal": [],
			"external": [],
		}
		message = mail.EmailMessage()

		if uri == "sendmail/deadlink":
			badurl = self.request.get("badurl").encode('utf-8', 'xmlcharrefreplace')
			message.subject = "Missing resource reported by user"
			message.body = templates.get("404","txt","email").format(**locals())
			messages["internal"].append(message)

		elif uri == "sendmail/changerequest":

			# performs rudimentary checks before sending mail. will not catch but the most basic weirdness.
			account_name = self.request.get("account_name").encode('utf-8', 'xmlcharrefreplace')
			student_name = self.request.get("student_name").encode('utf-8', 'xmlcharrefreplace')

			if account_name and student_name:

				message.subject = "Lesson Change Request for %s" % (student_name)

				lesson_date = self.request.get("lesson_date").encode('utf-8', 'xmlcharrefreplace')
				lesson_time = self.request.get("lesson_time").encode('utf-8', 'xmlcharrefreplace')
				comment = self.request.get("comment").encode('utf-8', 'xmlcharrefreplace')
				if not comment:
					comment = "(none)"

				if lesson_date or lesson_time:
					# still send the message if either date or time was missed
					message.body = templates.get("change_all","txt","email").format(**locals())
	
				else:
					requested_action = self.request.get("requested_action").encode('utf-8', 'xmlcharrefreplace')
					message.body = templates.get("change_one","txt","email").format(**locals())

				messages["internal"].append(message)

		elif uri == "sendmail/policyacceptance":
			signature_name = self.request.get("signature_name").encode('utf-8', 'xmlcharrefreplace')
			signature_email = self.request.get("signature_email").encode('utf-8', 'xmlcharrefreplace')
			policy_content_text  = self.request.get("policy_content_text").encode('utf-8', 'xmlcharrefreplace')
			policy_content_html  = self.request.get("policy_content_html").encode('utf-8', 'xmlcharrefreplace')
			photo_release = self.request.get_all("photo_release")
			photo_release = ', '.join(photo_release)

			if not photo_release:
				photo_release = "None - Do not publish my likeness without consent"

			signature_first = signature_name.split(" ")[0]
			signature_last = signature_name.split(" ")[1]

			message.subject = "Policy Accepted: %s, %s" % (signature_last, signature_first)
			message.body = templates.get("policyacceptance_internal","txt","email").format(**locals())

			messages["internal"].append(message)

			message_tocustomer = mail.EmailMessage()

			message_tocustomer.subject = "Rocketeria Music Lessons Policies"
			message_tocustomer.body = templates.get("policyacceptance_external","txt","email").format(**locals())
			message_tocustomer.html = templates.get("policyacceptance_external","html","email").format(**locals())
			message_tocustomer.to = signature_email

			messages["external"].append(message_tocustomer)


		elif uri == "sendmail/enroll":

			billto_firstandlast = self.request.get("billto_firstandlast").encode('utf-8', 'xmlcharrefreplace')
			billto_email = self.request.get("billto_email").encode('utf-8', 'xmlcharrefreplace')
			billto_mobilephone = self.request.get("billto_mobilephone").encode('utf-8', 'xmlcharrefreplace')
			billto_altphone = self.request.get("billto_altphone").encode('utf-8', 'xmlcharrefreplace')
			billto_address1 = self.request.get("billto_address1").encode('utf-8', 'xmlcharrefreplace')
			billto_address2 = self.request.get("billto_address2").encode('utf-8', 'xmlcharrefreplace')

			student_same_as_bill_to = self.request.get("student_same_as_bill_to").encode('utf-8', 'xmlcharrefreplace')

			if student_same_as_bill_to == "true":
				student_same_as_bill_to = "Yes"
				student_info = ""
			else:
				student_same_as_bill_to = "No"

				for n in range(3):
					n = n + 1
					if self.request.get("student%s_firstandlast" % n):
						student_firstandlast = self.request.get("student%s_firstandlast" % n).encode('utf-8', 'xmlcharrefreplace')
						student_email = self.request.get("student%s_email" % n).encode('utf-8', 'xmlcharrefreplace')
						student_mobilephone = self.request.get("student%s_mobilephone" % n).encode('utf-8', 'xmlcharrefreplace')
						student_altphone = self.request.get("student%s_altphone" % n).encode('utf-8', 'xmlcharrefreplace')
						student_school = self.request.get("student%s_school" % n).encode('utf-8', 'xmlcharrefreplace')
						student_grade = self.request.get("student%s_grade" % n).encode('utf-8', 'xmlcharrefreplace')
						try:
							student_info += templates.get("enroll_student_info","txt","email").format(**locals())
						except NameError:
							student_info = templates.get("enroll_student_info","txt","email").format(**locals())

				try:
					student_info
				except UnboundLocalError:
					student_info = "(no student info provided)"

			lesson_environment = self.request.get_all("lesson_environment")
			lesson_environment = ', '.join(lesson_environment)
			lesson_environment = lesson_environment.encode('utf-8', 'xmlcharrefreplace')

			instrument = self.request.get_all("instrument")
			instrument = ', '.join(instrument)
			instrument = instrument.encode('utf-8', 'xmlcharrefreplace')

			expertise = self.request.get_all("expertise")
			expertise = ', '.join(expertise)
			expertise = expertise.encode('utf-8', 'xmlcharrefreplace')

			teacher = self.request.get_all("teacher")
			teacher = ', '.join(teacher)
			teacher = teacher.encode('utf-8', 'xmlcharrefreplace')

			recurrence = self.request.get("recurrence").encode('utf-8', 'xmlcharrefreplace')

			day_of_week = self.request.get_all("day_of_week")
			day_of_week = ', '.join(day_of_week)
			day_of_week = day_of_week.encode('utf-8', 'xmlcharrefreplace')

			time_range = self.request.get_all("time_range")
			time_range = ', '.join(time_range)
			time_range.encode('utf-8', 'xmlcharrefreplace')

			comment1 = self.request.get("comment1").encode('utf-8', 'xmlcharrefreplace')
			if not comment1:
				comment1 = "(none)"

			photo_release = self.request.get_all("photo_release")
			photo_release = ', '.join(photo_release)
			photo_release = photo_release.encode('utf-8', 'xmlcharrefreplace')
			if not photo_release:
				photo_release = "None - Do not publish my likeness without consent"

			message.subject = "Enroll Form Submission: %s" % (billto_firstandlast)

			message.body = templates.get("enroll","txt","email").format(**locals())

			messages["internal"].append(message)

		for m in messages["internal"]:
			try:
				message = templatify_internal(message = m, remote_addr = self.request.remote_addr, remote_ua = self.request.headers['User-Agent'])
			except AttributeError:
				self.error(400)
			else:
				self.response.set_status(200)
				message.send()
		
		for m in messages["external"]:
			try:
				message = templatify_external(message = m)
			except AttributeError:
				self.error(400)
			else:
				self.response.set_status(200)
				message.send()
		
		self.redirect("/") # just for noscript


application = webapp2.WSGIApplication([
	(r'/sendmail/.*', MailHandler),
], debug=False)


