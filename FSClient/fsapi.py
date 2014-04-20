import json
from google.appengine.api import urlfetch

#apiroot = 'https://rocketeria2.fullslate.com/api'
apikey = 'aDbvS9DsQowbPhs9dfDxtEqsLCyZuVH9eaKHLtTsWLOpFe2wEq'
headers = { 'Content-Type': 'application/json',
			'Authorization' : 'Bearer %s' % (apikey),
			'User-Agent' : "Rocketeria FullSlate Interface Development Server | kyle{@}rocketeria{.}biz "
		  }

def apirequest(resource = '', post = None, secure = True, fs_server = "rocketeria2", apiroot = "api"):
	'''return response from POST to apiroot/apichild'''

	'''
	this should be made in to a class after PoC
	'''

	if not secure:
		protocol = "http"
	else:
		protocol = "https"


	url = "%s://%s.fullslate.com/%s/%s" % (protocol, fs_server, apiroot, resource)

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
		print "URLFETCH ERROR IN FSAPI.APRREQUEST: ",e
	except urlfetch.DownloadError as e:
		#response.content = ""
		print "URLFETCH ERROR IN FSAPI.APRREQUEST: ",e
	except urlfetch.SSLCertificateError as e:
		print "URLFETCH ERROR IN FSAPI.APRREQUEST: ",e
		#response.content = ""

	return response


