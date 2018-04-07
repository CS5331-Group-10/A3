import requests
import ssci
import oRedirect 

BASE_URL = "http://target.com/"

def injectPayload(url, paramname, method, payload, verbose = False):
	#finds index.php at base
	parsedURL = BASE_URL + url	
	html = ""	
	#if get
	if method == "GET":
		getURL = parsedURL + "?" + paramname+"="+payload[0]
		content = requests.get(getURL)
		html =  content.text

	#if post
	elif method == "POST":
		print("POST")

	result = checkSuccess(html, payload[1], content, verbose)
	if result is not None:
		print payload
		return payload

def checkSuccess(html, attackType, content, v=False):
	if v == True:
		print html

	if attackType == "Open Redirect":
		if len(content.history) > 0 and content.url == "https://status.github.com/messages":
			return True

	#server side injection:
	if attackType == "SSCI":
		#included index.php
		indexPHP = requests.get(BASE_URL + "index.php")
		if indexPHP.text in html:
			return attackType
		#uname -a successful:
		if "GNU/Linux" in html:
			return attackType

	return None;
	

if __name__ == "__main__":
	#Test for server side code injection
	'''
	url = "/serverside/eval2.php"
	payloads = ssci.get_all(url)
	for payload in payloads:
		injectPayload(url, "page", "GET", payload)
	'''
	#test for open redirect
	url = "/openredirect/openredirect.php"
	orPayload = oRedirect.get_all()
	for payload in orPayload:
		injectPayload(url, "redirect", "GET", payload)
