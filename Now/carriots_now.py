# Carriots Utilities - Now
# By Timothy D. Swieter, P.E.
# MIT License

# Access Carriots and pull down the latest time in various formats.
# See the following link for the API information:  https://www.carriots.com/documentation/api/dates
#
# NOTE:  You must add your API Key below.


import requests, json

# The setup for acceessing Carriots, enter your own API key
app_url = "http://api.carriots.com/"
app_element = "now/"
app_key = "ENTER_YOUR_API_KEY_HERE"

headers = {"carriots.apikey":app_key}

# Enter any parameters in the params section below or use one of the examples provided
params = {}                        						# defaults of date in ISO8601 based at UTC
#params = {'type':'timestamp'}     			 			# returns the unix based timestamp, format and time_zone are ignored
#params = {'type':'date', 'format':'Y-m-d'}             # returns just the date, no time
#params = {'type':'date', 'time_zone':'US/Eastern'}     # returns the full ISO8601 date/time for USA eastern timezone

print ""
print "Getting the date/time from Carriots..."

# Request, via the API, the time and store the json locally
carriotsResponse = requests.get(app_url + app_element, params=params, headers=headers)
binary = carriotsResponse.content
output = json.loads(binary)

print output
print "The URL used: " + carriotsResponse.url
print ""