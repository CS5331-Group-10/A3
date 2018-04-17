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
		params=b["post_params"]

	ep = b["endpoint"], b["get_post"], b["get_params"], b["post_params"]
	epList.append(ep)

payloads = ij.get_payloads()

for ep in epList:
	url = ep[0]
	for method in ep[1]:
		method = method.upper()
		if method == "GET":
			paramname = ep[2]
			for payload in payloads:
				if (ij.injectPayload(url,method,paramname,payload) == True):
					print url, payload
					
		elif method == "POST":
			for param in ep[3]:
				paramname = param
				for payload in payloads:
					if (ij.injectPayload(url,method,paramname,payload) == True):						print url, payload


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
