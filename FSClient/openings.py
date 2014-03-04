import datetime

def byday(openingobj):
	'''
	Return dict formatted { day of month : [opening,opening,] } for each object in OPENINGOBJ.
	OPENINGOBJ is list of datetime objects
	'''

	openingsbyday = {}

	for o in openingobj:

		dom = o.strftime('%d')
		hhmm = o.strftime('%I:%M %p')

		try:
			openingsbyday[dom] += [hhmm]
		except KeyError: # first element
			openingsbyday[dom] = [hhmm]

	return openingsbyday

def byday_full(openingobj):
	'''
	Return dict formatted { day of month : [{opening},{opening},], } for each object in OPENINGOBJ.
	OPENINGOBJ is list of fullslate event objects with date strings, OR
	a list of datetime objects
	replaced with datetime objects

	THIS FUNCTION ACCOMODATES FULL EVENT OBJECTS.
	ALL OTHER SCHEIPTS SHOULD BE MODIFIED TO USE THIS FUNCTION
	AT THAT POINT, REMOVE "-FULL" FROM THE NAME
	'''

	openingsbyday = {}

	for o in openingobj:

		try:
			dom = o['occurrence_at'].strftime('%d') # it was a fullslate event
		except TypeError: # no ['at'] - it's a list of datetime objects
			dom = o.strftime('%d')
		#print "\nDOM FROM OPENINGS.BYDAY_FULL: ",dom

		try:
			openingsbyday[dom].append(o)
		except KeyError: # first element
			openingsbyday[dom] = [o]

	return openingsbyday