# Carriots Utilities - Steams to CSV
# By Timothy D. Swieter, P.E.
# MIT License

# Access Carriots and pull down the streams within the date range and device specified.
# Process those streams into a CSV file and save locally.
# Feel free to tinker with the code to get the JSON to CSV translation you would like.
#
# NOTE:  You must add your API Key below and update the CSV Header row and CSV building routine to match your desired output.


import requests, json, csv
import datetime as dt


# Kick off the program by getting the user input and echo back
print ""
print "This program will build CSVs with data from Carriots."
print ""
deviceRI = raw_input("Please enter the name of the device in form test@Carriots: ").strip()
dateStartRI = raw_input("Please enter the date of the first day of data in form YYYY-MM-DD: ").strip()
dateEndRI = raw_input("Please enter the date of the last day of data in form YYYY-MM-DD: ").strip()
timezoneRI = raw_input("Please input your timezone offset such as -5 or +8: ").strip()

print ""
print "Data will be gathered for " + deviceRI + " from " + dateStartRI + " to " + dateEndRI

# Build the file name
fileName = dateStartRI + " " + deviceRI + ".csv"

# Calculate the time timestamps.
epochStart = dt.datetime(1970,1,1)

dateStartRI = dt.datetime.strptime(dateStartRI, '%Y-%m-%d')
timestampStart = int((dateStartRI - epochStart).total_seconds() - (int(timezoneRI) * 60 * 60))
# print timestampStart

dateEndRI = dt.datetime.strptime(dateEndRI, '%Y-%m-%d')
timestampEnd = int((dateEndRI - epochStart).total_seconds() - (int(timezoneRI) * 60 * 60) + (((23 * 60) + 59) * 60) + 59)
# print timestampEnd

# Prepare a CSV file for writing to.  
# Add, change and expand "data" to include names of values your device streams.
# This first row is a header in the CSV.
myCSV = csv.writer(open(fileName, "wb+"))
myCSV.writerow(["id_developer", 
			    "created_at", 
			    "at", 
			    "protocol", 
			    "owner", 
			    "device",
                "data"
                ])
totalRowsWritten = 1

# The setup for acceessing Carriots, enter your own API key
app_url = "http://api.carriots.com/"
app_element = "streams/"
app_key = "ENTER_YOUR_API_KEY_HERE"

headers = {"carriots.apikey":app_key}

# Loop through each hour and show how many streams there are (getting data from Carriots) and put into CSV
print ""
for hr in xrange(timestampStart, timestampEnd, 3600):
    at_from = hr
    at_to = hr + 3600

    # Adjust parameters for sorting or display per your own preferences
    params = {'device':deviceRI, 'at_from':at_from, 'at_to':at_to, 'sort':'at'}

	# Request, via the API, the streams and store the json locally
    carriotsResponse = requests.get(app_url + app_element, params=params, headers=headers)
    binary = carriotsResponse.content
    output = json.loads(binary)

    # Add,change and expand 'data' to match your device stream (this should also match the CSV header)
    for stream in range(len(output['result'])):

        myCSV.writerow([output['result'][stream]['id_developer'],
                        output['result'][stream]['created_at'],
                        output['result'][stream]['at'],
                        output['result'][stream]['protocol'],
                        output['result'][stream]['owner'],
                        output['result'][stream]['device'],
                        output['result'][stream]['data']
                        ])
                        # If you would like to use a specific value from the stream heirarchy, your lines above may look like the one below
                        # output['result'][stream]['data']['node']['voltage']

        totalRowsWritten += 1

    print (dt.datetime.fromtimestamp(at_from + (int(timezoneRI) * 60 * 60)).strftime('%Y-%m-%d Hour: %H')) + " has " + str(len(output['result'])) + " streams."

print ""
print "There were " + str(totalRowsWritten) + " rows created in the CSV"
print "The file name is: " + fileName
print ""