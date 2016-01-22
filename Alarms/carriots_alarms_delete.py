# Carriots Utilities - Alarms Delete
# By Timothy D. Swieter, P.E.
# MIT License

# Access Carriots and pull down a list of all alarms based on any parameters specified.
# Then attempt to delete each alarm.  Display the interaction on the terminal.
# See the following link for the API information:  https://www.carriots.com/documentation/api/alarms

# NOTE:  You must add your API Key below.

import requests, json

# The setup for acceessing Carriots, enter your own API key
app_url = "http://api.carriots.com/"
app_element = "alarms/"
app_key = "ENTER_YOUR_API_KEY_HERE"

headers = {"carriots.apikey":app_key}

# Enter any filter parameters in the params section below to limit which alarms are retreived
# Example:  {'device': 'example@carriots'}
params = {}


print ""
print "Getting alarms from Carriots..."

# Request, via the API, the alarms and store the json locally
carriotsResponse = requests.get(app_url + app_element, params=params, headers=headers)
binary = carriotsResponse.content
output = json.loads(binary)


# Uncomment the following if you wish to see the specific alarms retreived
#Print "The following are the alarms retreived"
#print output


print "There are " + str(len(output['result'])) + " alarms retrieved from Carriots."
print "Deleting each alarm..."


success = 0
fail = 0

for alarm in range(len(output['result'])):
    carriotsResponse = requests.delete(app_url + app_element + output['result'][alarm]['id_developer'] + "/", headers=headers)

    if carriotsResponse.status_code == requests.codes.ok:
        success += 1
    else:
        fail += 1


print ""
print "Total alarms deleted: " + str(success)
print "Total alarms unable to delete: " + str(fail)
print ""