import sys
import payloads.inject as ij
import json

json_data = open("result.json","r")
data = json.load(json_data)
target = "http://target.com"

#READ JSON
epList = list()
for b in data:
	params = 0
	ep = b["endpoint"], b["get_post"], b["get_params"], b["post_params"]
	epList.append(ep)

#READ PAYLOADs
payloads = ij.get_payloads()

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

def getId(expClass):
	if expClass == ij.sql_injection:
		return 0
	elif expClass == ij.server_injection:
		return 1
	elif expClass == ij.directory_traversal:
		return 2
	elif expClass == ij.open_redirect:
		return 3
	elif expClass == ij.cross_site_request_forgery:
		return 4
	elif expClass == ij.shell_command:
		return 5
	
#POPULATE JSON
for payload in payloads:
	for ep in epList:
		url = ep[0]

		for method in ep[1]:
			method = method.upper()
			if method == "GET":
				for param in ep[2]:
					if (ij.injectPayload(url,method,param,payload) == True):
						listExploits[getId(payload[1])]["results"][target].append(
						{
							"url": url,
							"params":{param:payload[0]},
							"method": method
						})		
	
			elif method == "POST":
				for param in ep[3]:
					if (ij.injectPayload(url,method,param,payload) == True):
						listExploits[getId(payload[1])]["results"][target].append(
						{
							"url": url,
							"params":{param:payload[0]},
							"method": method
						})		


print listExploits

def timeid(full=False):
	if full==False:
		return datetime.now().strftime("%S-%f")
	else:
		return datetime.now().strftime("%H-%M-%S-%f") 

def generateExploit(url, method, paramname, payload):
#payload is a "payload, type_of_payload" list

	dirname = "exploits/"
	if not os.path.exists(dirname):
		os.makedirs(dirname)

	copy("exploit.py", dirname)

	f = open(dirname + payload[1] + "_" + timeid() + ".sh","w+")
	f.write("python exploit.py " + '"' + url +'" ' + method + " "+ paramname + ' "' +payload[0]+'"')
	



#for each endpoint in JSON, get ENDPOINT, PARAMS, METHOD [TBC: Zishan]
	#for each payload, [TBC: Zhizhong]
		#run injectPayload(url, paramname, method, payload) [DONE]	
		#currently, this code prints out the payload if successful, and writes a 		dummy .sh file [TBC: Jason]

#Once above is all completed, consolidate result in a .JSON file [TBC: WY]
