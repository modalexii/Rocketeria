import webapp2

class FetchHandler(webapp2.RequestHandler):

	def get(self, *args, **kwargs):
		import cloudstorage
		from urllib import unquote

		uri = self.request.path
		uri = unquote(uri.encode('ascii')).decode('utf-8')

		try:
			gcs_object = cloudstorage.open(
				uri,
				mode = "r",
			)
		except cloudstorage.NotFoundError:
			self.response.set_status(404)
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

