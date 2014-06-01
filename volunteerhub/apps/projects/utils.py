import json
import urllib


def get_lat_long(location):
    location = urllib.quote_plus(location)
    request = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % location
    try:
        response = urllib.urlopen(request)
    except:
        return ''

    data = json.load(response)
    try:
        coords = data['results'][0]['geometry']['location']
        return "%s, %s" % (coords['lat'], coords['lng'])
    except:
        return ''
