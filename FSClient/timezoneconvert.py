'''
This is mostly a bunch of wrappers for consistancy. It will probably help
scale the application at a later date.

EST = timezoneconvert.abbr2zone("EST")
GMT = EST = timezoneconvert.abbr2zone("GMT")
today = datetime.datetime.today()
today = timezoneconvert.set(today,GMT)
today = timezoneconvert.convert(today,EST)
'''

from datetime import datetime,tzinfo,timedelta

class Zone(tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
        return timedelta(hours=1) if self.isdst else timedelta(0)
    def tzname(self,dt):
        return self.name

def abbr2zone(abbr):
    '''
    given a string appreviation for a time zone, return the 
    Zone object from Zone
    '''
    if abbr == "GMT":
       return Zone(0,False,'GMT') 
    elif abbr == "EST":
        return Zone(-5,False,'EST')

def set(dto,zone):
    '''
    Set tzinfo on datetime object DTO to ZONE
    '''
    return dto.replace(tzinfo=zone)

def convert(dto,zone):
    '''
    Convert a datetime object DTO to ZONE
    OBJECT is assumed to have tzinfo set already
    '''
    return  dto.astimezone(zone)
