def getFSclient(email):
	'''Return the fullSlate client object with an email address matching EMAIL'''
	'''if no match is found, raise NoSuchClient exception'''
	import faspi
	import json
	import pprint

	# get all valid IDs
	clientobj = fsapi.apirequest('clients')
	clientobj = json.loads(clientobj)
	pprint.pprint(clientobj)
	valid_ids = [c['id'] for c in clientobj]
	pprint(valid_ids)

	# get the emails for each of those IDs
	for i in valid_ids:
		fsclient = fsapi.apirequest('clients/%s' % i)
		if fsclient['success'] == True:
			fsclient_emails = fsclient['emails']
			for e in fsclient_emails:
				if e['address'] == email:
					return fsclient
		else:
			pass

	raise Exception('NoSuchClient')

def getclientevents(id,after=None,before=None):
	'''Return list of event objects attended by ID between AFTER and BEFORE/
	If AFTER or BEFORE is omitted, FullSlate returns all events less than one
	month from today, or as filtered by either AFTER or BEFORE'''