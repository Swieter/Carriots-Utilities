# Carriots Utilities - Device Update
# By Timothy D. Swieter, P.E.
# MIT License

# Access Carriots and pull down the device list.
# Process that list to update the property in each device.
# See the following link for the API information:  https://www.carriots.com/documentation/api/device_management
#
# NOTE:  You must add your API Key below and add the details for how you want the device to be updated.


import requests, json


# The setup for acceessing Carriots, enter your own API key
app_url = "http://api.carriots.com/"
app_element = "devices/"
app_key = "ENTER_YOUR_API_KEY_HERE"

headers = {"carriots.apikey":app_key}

print ""
print "Getting devices from Carriots..."

# Enter any filter parameters in the params section below to limit which devices are retreived
# Example:  {'device': 'example@carriots'}
params = {}

# Request, via the API, the streams and store the json locally
carriotsResponse = requests.get(app_url + app_element, params=params, headers=headers)
binary = carriotsResponse.content
output = json.loads(binary)


# Uncomment the following if you wish to see the specific device list retreived
#Print "The following are the devices retreived"
#print output


print "There are " + str(len(output['result'])) + " devices retrieved from Carriots."
print "Updating each device..."


success = 0
fail = 0


for device in range(len(output['result'])):

	print output['result'][device]

	# Place here the aspects of device you would like to update, there are some core required elemnets in each put, those are included below.
	updateValues = {'type': output['result'][device]['type'],
				   'name': output['result'][device]['name'],
				   'id_assets': output['result'][device]['id_assets'],
				   'id_group': output['result'][device]['id_group'],
				   'enabled': output['result'][device]['enabled'],
				   'id_developer': output['result'][device]['id_developer'],
				   'id_model': output['result'][device]['id_model'],
				   }

	carriotsResponse = requests.put(app_url + app_element + output['result'][device]['id_developer'] + "/", headers=headers, data=json.dumps(updateValues))

	if carriotsResponse.status_code == requests.codes.ok:
		success += 1
	else:
		fail += 1


print ""
print "Total devices updated: " + str(success)
print "Total devices unable to update: " + str(fail)
print ""