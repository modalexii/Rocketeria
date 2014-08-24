import webapp2,logging

logging.getLogger().setLevel(logging.INFO)

def clear_banner(handler):
	# Check if an alert banner needs to be cleared
	import gae_db

	try:
		banner = gae_db.fetch_content(uri = "/banner")
	except AttributeError as e:
		logging.info("cronjob clear_banner found no banner")
		return

	expiry = banner.split("--")[1] # the html comment guts
	expiry = expiry.split("%")[1] # our arbitratily selected delimiter

	from datetime import datetime

	try:
		expiry = datetime.strptime(expiry,"%d/%m/%YT%H:%M:%S")
	except ValueError:
		# exipry does not match the strptime format - it is probably ""
		logging.info("cronjob clear_banner found a non-expiring banner (expiry was \"%s\")" % expiry)
		return

	now = datetime.now()

	if now > expiry: # expiry was entered in UTC, no need to convert anything here
		gae_db.delete_page("/banner")
		logging.info("cronjob clear_banner removed an alert banner set to expire on %s" % expiry)
	else:
		logging.info("cronjob clear_banner found banner that has not expired yet - it will expire \"%s\"" % expiry)


class CronHandler(webapp2.RequestHandler):

	def get(self):
		'''handle HTTP GETs'''

		request_path = self.request.path.strip('/')

		if request_path == "cron/bihourly":
			
			clear_banner(self)


application = webapp2.WSGIApplication([
	('/cron/?.*', CronHandler),
], debug=False)