import sys
import payloads.inject as ij
import json

json_data = open("result.json","r")
data = json.load(json_data)
target = ij.BASE_URL

#READ JSON
epList = list()
for eps in data:
	for ep in eps["endpoints"]:
		epList.append(ep)

#prepare results list
listExploits = list()
for x in range(6):
	listExploits.append({"class": "", "results": { target: list()}})

listExploits[0]["class"] = ij.sql_injection
listExploits[1]["class"] = ij.server_injection
listExploits[2]["class"] = ij.directory_traversal
listExploits[3]["class"] = ij.open_redirect
listExploits[4]["class"] = ij.cross_site_request_forgery
listExploits[5]["class"] = ij.shell_command

#READ PAYLOADs
payloads = ij.get_payloads()
#inject payloads and populate json
for payload in payloads:
	
	for ep in epList:
		endpoint = ep["endpoint"]
		method = ep["method"]
		params = ep["param"]
		values = ep["value"]
		pvPair = dict(zip(params,values))
		method = method.upper()	
		params = [p.replace("_hiddenPEST","") for p in params]
		for param in params:	
			if (ij.injectPayload(endpoint,method,param,pvPair,payload) == True):
				pvPair[param]=payload[0]
				listExploits[ij.getId(payload[1])]["results"][target].append(
				{
					"endpoint": endpoint,
					"params": pvPair,
					"method": method
				})		

#handle csrf
#We are saying that as long as there is a hidden value in the form, it is a CSRF. 
#therefore: high false positive rates?
for ep in epList:
	hidden = False
	success = False
	params = ep["param"]
	endpoint = ep["endpoint"]
	method = ep["method"]
	params = ep["param"]
	values = ep["value"]
	for param in params:
		if "_hiddenPEST" in param:
			hidden=True
	
	params = [p.replace("_hiddenPEST","") for p in params]
	pvPair = dict(zip(params,values))
	if hidden==True:
	#check successs
		success= True

	if success==True:
		listExploits[ij.getId(ij.cross_site_request_forgery)]["results"][target].append(
		{
			"endpoint": endpoint,
			"params": pvPair,
			"method": method
		})


#write json
with open("vuln.json", "w") as f:
	f.write(json.dumps(listExploits, indent=4))
