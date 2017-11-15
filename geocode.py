import httplib2
import json

def getGeocodeLocation(inputString):
    google_api_key = "AIzaSyBy8kXiEm-1qdGRahIHrx1_jTxM8pn5ErQ"
    locationString = inputString.replace("", "+")
    url = ('https://maps.googleapis.com/maps/geocode/json?address=%s&key%s'%(locationString, google_api_key))
    h = httplib2.Http()
    response, content = h.request(url,'GET')
    result = json.loads(content)
    print "response header: %s \n \n" % response
