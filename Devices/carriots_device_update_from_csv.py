# Carriots Utilities - Device Update From CSV
# By Timothy D. Swieter, P.E.
# MIT License

# Take a CSV file with details for new devices or modifying devices.
# Process that file to create or modify devices on Carriots.
# See the following link for the API information:  https://www.carriots.com/documentation/api/device_management
#
# NOTE:  You must add your API Key below


import requests, json, csv

# Kick off the program by getting the user input
print ""
print "This program will take a CSVs of device details and update Carriots."
print ""
csvFileRI = raw_input("Please enter the name of the CSV file: ").strip()
print ""

# Open the file and prepare to process
myCSVfile = open(csvFileRI, 'rU')
myCSVreader = csv.reader(myCSVfile, delimiter = ',')
myCSVdata = list(myCSVreader)
myCSVdataFiltered = []

for row in myCSVdata:

	# Create any filters here such as skipping first row
	# This filters out items in the first column with a short name
	if len(row[0]) < 35:
		continue

	myCSVdataFiltered.append(row)

myCSVfile.close()

print "File opened, read and closed"
print "There are " + str(len(myCSVdataFiltered)) + " rows to be processed."


# The setup for acceessing Carriots, enter your own API key
app_url = "http://api.carriots.com/"
app_element = "devices/"
app_key = "ENTER_YOUR_API_KEY_HERE"

headers = {"carriots.apikey":app_key}

#print ""
#print "Processing the file to Carriots"

successCarriots = 0
failCarriots = 0

for row in myCSVdataFiltered:
	# set up a filter for finding a specific device
	# It is assumed the first column of the CSV has the developer ID in it
	params = {'id_developer': row[0]}
	#print params

	print "Processing device: " + row[0]

	# Request, via the API, the device and store the json locally
	carriotsResponse = requests.get(app_url + app_element, params=params, headers=headers)
	binary = carriotsResponse.content
	output = json.loads(binary)

	#print output
	#print ""

	# Process results from carriots to modify or create a new device
	if output['total_documents'] == 1:
		updateValues = output['result'][0]

		# It is assumed the CSV is set up in this order, you can add or change columns as you wish
		updateValues['id_group'] = row[1]
		updateValues['id_assets'] = row[2]
		updateValues['id_model'] = row[3]
		updateValues['name'] = row[4]
		updateValues['description'] = row[5]
		updateValues['time_zone'] = row[6]
		updateValues['frequency_stream'] = int(row[7])
		updateValues['frequency_status'] = int(row[8])
		updateValues['type'] = row[9]
		updateValues['enabled'] = bool(row[10])

		# Example if using the user specified device properties, likely need to add key
		#updateValues['properties'] = {}
		#updateValues['properties']['SerialNumber'] = row[7]


		# Send updated values to Carriots
		carriotsResponse = requests.put(app_url + app_element + updateValues['id_developer'] + "/", headers=headers, data=json.dumps(updateValues))

		#print carriotsResponse.status_code
		#print carriotsResponse.text

		if carriotsResponse.status_code == requests.codes.ok:
			successCarriots += 1
		else:
			failCarriots += 1

	elif output['total_documents'] == 0:
		createValues = {}

		# It is assumed the CSV is set up in this order, you can add or change columns as you wish
		createValues['id_developer'] = row[0]
		createValues['id_group'] = row[1]
		createValues['id_assets'] = row[2]
		createValues['id_model'] = row[3]
		createValues['name'] = row[4]
		createValues['description'] = row[5]
		createValues['time_zone'] = row[6]
		createValues['frequency_stream'] = int(row[7])
		createValues['frequency_status'] = int(row[8])
		createValues['type'] = row[9]
		createValues['enabled'] = bool(row[10])

		# Example if using the user specified device properties, likely need to add key
		#updateValues['properties'] = {}
		#updateValues['properties']['SerialNumber'] = row[7]


		# Send updated values to Carriots
		carriotsResponse = requests.post(app_url + app_element, headers=headers, data=json.dumps(createValues))

		print carriotsResponse.status_code
		print carriotsResponse.text

		if carriotsResponse.status_code == requests.codes.ok:
			successCarriots += 1
		else:
			failCarriots += 1

print ""
print "Total devices updated: " + str(successCarriots)
print "Total devices unable to update: " + str(failCarriots)
print ""
