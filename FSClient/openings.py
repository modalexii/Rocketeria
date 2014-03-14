import datetime

def byday(openingobj):
	'''
	Return dict formatted { day of month : [{opening},{opening},], } for each object in OPENINGOBJ.
	OPENINGOBJ is list of fullslate event objects with date strings, OR
	a list of datetime objects
	replaced with datetime objects

	'''

	openingsbyday = {}

	for o in openingobj:

		try:
			dom = o['occurrence_at'].strftime('%d') 
			# it was a fullslate event
		except TypeError: 
			# no ['occurrence_at'] - it's a list of datetime objects
			# OR a recurring fullslate object (may mean our API call is messed up)
			dom = o.strftime('%d')
		#print "\nDOM FROM OPENINGS.BYDAY_FULL: ",dom

		try:
			openingsbyday[dom].append(o)
		except KeyError: # first element
			openingsbyday[dom] = [o]

	return openingsbyday