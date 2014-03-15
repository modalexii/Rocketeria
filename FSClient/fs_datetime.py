def tz_convert(dto, from_zone, to_zone):
	'''
	Change datetime object DTO from tz object FROM_ZONE 
	to tz object TO_ZONE
	Returns datetime object
	'''
	from pytz.gae import pytz
	from datetime import datetime
	is_currently_dst = currently_dst(to_zone)
	from_zone, to_zone = pytz.timezone(from_zone), pytz.timezone(to_zone)
	return from_zone.localize(dto, is_dst=is_currently_dst).astimezone(to_zone)

def currently_dst(zonename):
	''' 
	Return Bool indicating if ZONENAME is currently
	in daylight zavings
	ZONENAME is string like "America/New_York"
	'''
	import pytz.gae
	from datetime import datetime, timedelta
	tz = pytz.timezone(zonename)
	now = pytz.utc.localize(datetime.utcnow())
	return now.astimezone(tz).dst() != timedelta(0)

def normalize(in_string,in_format,from_zone=None,to_zone=None):
	'''
	Take the various date & time strings given by FullSlate
	and return a standard python datatime object.
	IN_STRING is the date or time string to convert
	IN_FORMAT is a string explaining STRING's format using
	the strftime syntax
	FROM_ZONE is the time zone (string like "America/New_York") to associate 
	with the data as-is
	TO_ZONE is the zone (string like "America/New_York") to convert the
	data to
	FROM_ZONE and TO_ZONE must both be specified to have an effect
	'''
	from datetime import datetime
	dto = datetime.strptime(in_string,in_format)

	#print "\nFSDATETIME NORMALIZING: ",in_string

	if from_zone and to_zone:
		dto = tz_convert(dto,from_zone,to_zone)

	#print "\nFSDATETIME NORMALIZED: ",in_string
	return dto

def fullslateify(dto,out_format,from_zone=None,to_zone=None):
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

	if from_zone and to_zone:
		dto = tz_convert(dto,from_zone,to_zone)

	return dto.strftime(out_format)