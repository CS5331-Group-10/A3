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
	
	html = content.text
	result = checkSuccess(html, payload, content, parsedURL, method, paramname, params,verbose)
	
	#if function returns:
	if result is not None:
		print(url, payload)
		return True
	return None


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

def checkSuccess(html, payload, content, url, method, paramname,params, v=False):
	attackType = payload[1]
	#===== check for directory traversal =====
	if attackType == directory_traversal:
		match = re.findall(r'\w*\:\w\:[0-9]*\:[0-9]*\:[a-zA-Z_-]*\:[\/a-zA-Z0-9]*[ \t]?:[\/a-zA-Z0-9]*', html)
		if len(match) == 0:
			return None
		return match

	#======= check for shell command injection ======
	if attackType == shell_command:
		match = re.findall(r'GNU/Linux', html)
		if len(match) == 0:
			return None
		return match

	if attackType == sql_injection and len(content.history) == 0:

		params[paramname] = sqli.get_falsewy()
		#if get
		if method == "GET":
			paramstr = "&".join("%s=%s" % (k,v) for k,v in params.items())
			getURL = url + "?" + paramstr
			falseContent = requests.get(getURL)
		#if post
		elif method == "POST":
			falseContent = requests.post(url, data=params)

		falsehtml = falseContent.text
		falsehtml = falsehtml.replace(params[paramname],"")
		html = html.replace(payload[0],"")

		if falsehtml == html or len(falseContent.history)!=0 or abs(len(html)-len(falsehtml)) < 30:
			return None
		return True

		## for real sql injection, the payloads should return the same result
		## then compare the fake page with the true page to see the difference
		#falsePayloads = sqli.get_false()
		#if get
		#badhtml = []
		#for falsePayload in falsePayloads:
		#	if method == "GET":
		#		getURL = url + "?" + paramname+"="+falsePayload
		#		false_page = requests.get(getURL)
		#		if(false_page.status_code==200):
		#			badhtml.append(false_page.text)
		#		else:
		#			badhtml.append(requests.get(url).text)
		#	#if post
		#	elif method == "POST":
		#		false_page = requests.post(url, data={paramname:falsePayload})
		#		if(false_page.status_code==200):
		#			badhtml.append(false_page.text)
		#			# print(html)
		#		else:
		#			badhtml.append(requests.get(url).text)
		#if (badhtml[0] == badhtml[1]) and (badhtml[0] !=badhtml[2]):
		#	## true filter should be two
		#	compare_res = sqli.compare_html(badhtml[2], html)  
		#	match = re.findall(r'<ins>.+', compare_res)
		#elif(badhtml[0]==badhtml[2] and badhtml[0] !=badhtml[1]):
		#	compare_res = sqli.compare_html(badhtml[1], html)  
		#	match = re.findall(r'<ins>.+', compare_res)
		#else:
		#	match = ""
		# if(content.status_code==200) and badhtml[1]==html:
		#     compare_res = sqli.compare_html(badhtml[0], html)  
		#     match = re.findall(r'<ins>.+', compare_res)

		# else:
		#     match = ""
		#if len(match) ==0 :
		#	return None
		#
		#return match


	#====== check for open_redirect=======
	if attackType == open_redirect:
		if len(content.history) > 0 and content.url == "https://status.github.com/messages":
			return True

	
	#=======check for server_injection ====
	if attackType == server_injection and len(content.history) == 0 :
		#included index.php
		indexPHP = requests.get(BASE_URL + "/index.php")

		if indexPHP.text in html:
			return attackType
		#uname -a successful:
		if "GNU/Linux" in html:
			return attackType

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
				"/openredirect/openredirect.php"]
	for payload in payloads:
		injectPayload(url_list[0],  'GET','ascii', {"ascii":"cat","utf":"dog"},payload)
		injectPayload(url_list[1], 'POST', "host", {"host":""},payload)
		injectPayload(url_list[2],  "POST", "username", {"username":""}, payload)
		injectPayload(url_list[3],  "post", "page", {"page":""}, payload)
		injectPayload(url_list[4],  "GET", "redirect",{"redirect":""}, payload)
