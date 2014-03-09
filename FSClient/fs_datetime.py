'''
EST = timezoneconvert.abbr2zone("EST")
GMT = EST = timezoneconvert.abbr2zone("GMT")
today = datetime.datetime.today()
today = timezoneconvert.set(today,GMT)
today = timezoneconvert.convert(today,EST)
'''

def normalize(in_string,in_format,current_zone=None,changeto_zone=None):
	'''
	Take the various date & time strings given by FullSlate
	and return a standard python datatime object.
	IN_STRING is the date or time string to convert
	IN_FORMAT is a string explaining STRING's format using
	the strftime syntax
	CURRENT_ZONE is the time zone (abbreviation, string) to associate 
	with the data as-is (opt.)
	CHANGETO_ZONE is the zone (abbreviation, string) to convert the
	data to (opt.). Requires in_zone, OR tzinfo already set.
	'''
	from datetime import datetime
	dto = datetime.strptime(in_string,in_format)

	#print "\nFSDATETIME NORMALIZING: ",in_string

	if current_zone or changeto_zone:
		import timezoneconvert
		if current_zone:
			current_zone = timezoneconvert.abbr2zone(current_zone)
			dto = timezoneconvert.set(dto,current_zone)
		if changeto_zone:
			changeto_zone = timezoneconvert.abbr2zone(changeto_zone)
			dto = timezoneconvert.convert(dto,changeto_zone)

	return dto

def fullslateify(dto,out_format,current_zone=None,changeto_zone=None):
	'''
	Take a datetime object and return an equivilent string
	in the format that FullSlate expects
	DTO is a python datetime object
	OUT_FORMAT is a string explaining STRING's format using
	the strftime syntax
	CURRENT_ZONE is the time zone (abbreviation, string) to associate 
	with the data as-is (opt.)
	CHANGETO_ZONE is the zone (abbreviation, string) to convert the
	data to (opt.). Requires in_zone, OR tzinfo already set.
	'''
	if current_zone or changeto_zone:
		import timezoneconvert
		if current_zone:
			current_zone = timezoneconvert.abbr2zone(current_zone)
			dto = timezoneconvert.set(dto,current_zone)
		if changeto_zone:
			changeto_zone = timezoneconvert.abbr2zone(changeto_zone)
			dto = timezoneconvert.convert(dto,changeto_zone)

	return dto.strftime(out_format)