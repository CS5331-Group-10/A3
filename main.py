import sys
import payloads.inject
import json

json_data = open("result.json","r")
data = json.load(json_data)

for a in data[0]:
	print a

for b in data:
	print b["endpoint"], b["get_post"], b["query"]
#for each endpoint in JSON, get ENDPOINT, PARAMS, METHOD [TBC: Zishan]
	#for each payload, [TBC: Zhizhong]
		#run injectPayload(url, paramname, method, payload) [DONE]	
		#currently, this code prints out the payload if successful, and writes a 		dummy .sh file [TBC: Jason]

#Once above is all completed, consolidate result in a .JSON file [TBC: WY]
