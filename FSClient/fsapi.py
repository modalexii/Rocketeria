import json
from google.appengine.api import urlfetch

apiroot = 'https://rocketeria2.fullslate.com/api'
apikey = 'aDbvS9DsQowbPhs9dfDxtEqsLCyZuVH9eaKHLtTsWLOpFe2wEq'
headers = {'Content-Type': 'application/json', 'Authorization' : 'Bearer %s' % (apikey),}

def request(resource,post = None):
	'''return response from POST to apiroot/apichild'''
	url = "%s/%s" % (apiroot, (resource or ''),)
	
	try:
		response = urlfetch.fetch(
			url = url,
			payload = post,
			method = urlfetch.POST,
			headers = headers,
			validate_certificate = True,
			)
	except urlfetch.InvalidURLError as e:
		#response.content = ""
		print "ERROR" + e
	except urlfetch.DownloadError as e:
		#response.content = ""
		print "ERROR" + e
	except urlfetch.SSLCertificateError as e:
		print "ERROR" + e
		#response.content = ""

	return response


