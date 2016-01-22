# Carriots Utilities - Streams Delete
# By Timothy D. Swieter, P.E.
# MIT License

# Access Carriots and pull down a list of all streams based on any parameters specified.
# Then attempt to delete each stream.  Display the interaction on the terminal.
# See the following link for the API information:  https://www.carriots.com/documentation/api/data_management

# NOTE:  You must add your API Key below.

import requests, json

# The setup for acceessing Carriots, enter your own API key
app_url = "http://api.carriots.com/"
app_element = "streams/"
app_key = "ENTER_YOUR_API_KEY_HERE"

headers = {"carriots.apikey":app_key}

# Enter any filter parameters in the params section below to limit which streams are retreived
# Example:  {'device': 'example@carriots'}
params = {}


print ""
print "Getting streams from Carriots..."

# Request, via the API, the streams and store the json locally
carriotsResponse = requests.get(app_url + app_element, params=params, headers=headers)
binary = carriotsResponse.content
output = json.loads(binary)


# Uncomment the following if you wish to see the specific streams retreived
#Print "The following are the streams retreived"
#print output


print "There are " + str(len(output['result'])) + " streams retrieved from Carriots."
print "Deleting each stream..."


success = 0
fail = 0

for stream in range(len(output['result'])):
    carriotsResponse = requests.delete(app_url + app_element + output['result'][stream]['id_developer'] + "/", headers=headers)

    if carriotsResponse.status_code == requests.codes.ok:
        success += 1
    else:
        fail += 1


print ""
print "Total streams deleted: " + str(success)
print "Total streams unable to delete: " + str(fail)
print ""