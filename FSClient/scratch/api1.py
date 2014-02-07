import json


apiroot = 'http://stage.rocketeria2.fullslate.com/api'
apikey = 'aDbvS9DsQowbPhs9dfDxtEqsLCyZuVH9eaKHLtTsWLOpFe2wEq'

def apirequest(apichild):
	from urllib2 import urlopen
	url = "%s/%s?app=%s" % (apiroot, (apichild or ''), apikey)
	encodedjson = urlopen(url)
	decodedjson = json.load(encodedjson)
	return decodedjson


services = apirequest('services')

import pprint
pprint.pprint(services)
exit

for s in services:
	print s['name']

choice = raw_input("Which instrument? ")

choice = { s for s in services if s['name'] == 'choice' }
print "Here's some info about %s" % (choice['name']) 

