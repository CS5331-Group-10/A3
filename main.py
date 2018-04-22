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


#POPULATE JSON


for payload in payloads:
	
	for ep in epList:
		endpoint = ep["endpoint"]
		method = ep["method"]
		params = ep["param"]
		values = ep["value"]
		pvpair = dict(zip(params,values))
		method = method.upper()
		for param in params:
			if (ij.injectPayload(endpoint,method,param,pvpair,payload) == True):
				pvpair[param]=payload[0]
				listExploits[ij.getId(payload[1])]["results"][target].append(
				{
					"endpoint": endpoint,
					"params":pvpair,
					"method": method
				})		
with open("vuln.json", "w") as f:
	f.write(json.dumps(listExploits, indent=4))
