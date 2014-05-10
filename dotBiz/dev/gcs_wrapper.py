import webapp2
import handle_errors

class FetchHandler(webapp2.RequestHandler):

	def get(self, *args, **kwargs):
		import cloudstorage
		from urllib import quote

		uri = self.request.path

		try:
			gcs_object = cloudstorage.open(
				uri,
				mode = "r",
			)
		except cloudstorage.NotFoundError:
			handle_errors.http404(self.request, self.response)
		else:
			gcs_object_info = cloudstorage.stat(
				uri,
			)

			self.response.headers['Content-Type'] = gcs_object_info.content_type
			self.response.write(gcs_object.read())

			gcs_object.close()

application = webapp2.WSGIApplication([
	('/dres/.*', FetchHandler)
], debug=False)
