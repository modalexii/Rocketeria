import json
from google.appengine.api import urlfetch

apiroot = 'https://rocketeria2.fullslate.com/api'
apikey = 'aDbvS9DsQowbPhs9dfDxtEqsLCyZuVH9eaKHLtTsWLOpFe2wEq'
headers = { 'Content-Type': 'application/json',
			'Authorization' : 'Bearer %s' % (apikey),
			'User-Agent' : "Rocketeria FullSlate Interface Development Server | kyle{@}rocketeria{.}biz "
		  }

def apirequest(resource,post = None, http_method = "post"):
	'''return response from POST to apiroot/apichild'''
	url = "%s/%s" % (apiroot, (resource or ''),)
	
	if http_method == "post":
		urlfetch_method = urlfetch.POST
	elif http_method == "delete":
		urlfetch_method = urlfetch.DELETE

	try:
		response = urlfetch.fetch(
			url = url,
			payload = post,
			method = urlfetch_method,
			headers = headers,
			validate_certificate = True,
			)
	except urlfetch.InvalidURLError as e:
		#response.content = ""
		print "URLFETCH ERROR IN FSAPI.APRREQUEST: ",e
	except urlfetch.DownloadError as e:
		#response.content = ""
		print "URLFETCH ERROR IN FSAPI.APRREQUEST: ",e
	except urlfetch.SSLCertificateError as e:
		print "URLFETCH ERROR IN FSAPI.APRREQUEST: ",e
		#response.content = ""

	return response


