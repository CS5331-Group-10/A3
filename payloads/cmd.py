import re

def get_all():
	payloads = [";uname -a"]
	# payloads = [";uname -a",";ls -al", "; cat /etc/passwd"]

	payloads = [(item, "Shell Command Injection") for item in payloads]
	return payloads

def checkSuccess(html):
	match = re.findall(r'GNU/Linux', html)
	if len(match) == 0:
		return False
	return True
	
if __name__ == "__main__":	
	print get_all()
