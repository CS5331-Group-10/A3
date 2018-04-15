import sys
import payloads.inject
import json

json_data = open("result.json","r")
data = json.load(json_data)


#for each endpoint in JSON, get ENDPOINT, PARAMS, METHOD
	#for each payload,
		#run injectPayload(url, paramname, method, payload) [ALREADY IMPORTED]	
		#currently, this code prints out the payload if successful, and writes a 		dummy .sh file [probably buggy at this point]



#To be done: consolidate result in a .JSON file
