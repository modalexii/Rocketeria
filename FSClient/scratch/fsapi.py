import json
from urllib2 import urlopen

apiroot = 'http://stage.rocketeria2.fullslate.com/api'
apikey = 'aDbvS9DsQowbPhs9dfDxtEqsLCyZuVH9eaKHLtTsWLOpFe2wEq'

def apirequest(apichild):
	url = "%s/%s?app=%s" % (apiroot, (apichild or ''), apikey)
	try:
		encodedjson = urlopen(url)
		decodedjson = json.load(encodedjson)
	except URLError:
		decodedjson =  None
	finally:
		return decodedjson
