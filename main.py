import sys
import payloads.inject as ij
import json

json_data = open("result.json","r")
data = json.load(json_data)

#for a in data[0]:
#	print a

epList = list()
for b in data:
	params = 0
	if len(b["get_post"]) == 0:
		continue;
	elif (b["get_post"][0].upper() == "GET"):
		params=b["get_params"]
	else:
		params=b["post_params"]

	ep = b["endpoint"], b["get_post"], params
	epList.append(ep)

payloads = ij.get_payloads()
print payloads

print epList
#for each endpoint in JSON, get ENDPOINT, PARAMS, METHOD [TBC: Zishan]
	#for each payload, [TBC: Zhizhong]
		#run injectPayload(url, paramname, method, payload) [DONE]	
		#currently, this code prints out the payload if successful, and writes a 		dummy .sh file [TBC: Jason]

#Once above is all completed, consolidate result in a .JSON file [TBC: WY]
