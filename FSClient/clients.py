def fs_client_from(email):
	'''Return the fullSlate client object with an email address matching EMAIL'''
	'''if no match is found, raise NoSuchClient exception'''
	import fsapi
	import json
	import pprint

	# get all valid IDs
	clientobj = fsapi.apirequest('clients')
	clientobj = json.loads(clientobj.content)
	pprint.pprint(clientobj)
	valid_ids = [c['id'] for c in clientobj]
	pprint.pprint(valid_ids)

	# get the emails for each of those IDs
	for i in valid_ids:
		fsclient = fsapi.apirequest('clients/%s' % i)
		fsclient = json.loads(fsclient.content)
		if fsclient['success'] == True:
			fsclient_emails = fsclient['emails']
			for e in fsclient_emails:
				if e['address'] == email:
					return fsclient
		else:
			pass

	raise Exception('NoSuchClient')

def fs_events_attended(id,start=None,stop=None):
	'''
	Return list of event objects attended by ID between START and STOP.
	If START or STOP is omitted, FullSlate returns all events less than one
	month from today, or as filtered by either START or STOP.
	START/STOP format = yyyy-mm-dd e.g., 2014-02-14
	'''
	import fsapi
	import json
	import pprint

	if start or stop:
		post = {'start' : start, 'stop' : stop}
		post = json.dumps(post)
		pprint.pprint(post)
	else:
		post = None
	allevents = fsapi.apirequest('events',post)
	allevents = json.loads(allevents.content)

	interesting_events = []

	for e in allevents:
		try:
			for a in e[u'attendees']:
				print "############ A: ",a,'\n'
				if a[u'id'] == id:
					interesting_events.append(e)
		except KeyError: # no attendees
			pass

	return interesting_events
