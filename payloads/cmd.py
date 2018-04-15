
def get_all():
	payloads = [";uname -a"]
	# payloads = [";uname -a",";ls -al", "; cat /etc/passwd"]

	payloads = [(item, "Shell Command Injection") for item in payloads]
	return payloads
	
if __name__ == "__main__":	
	print get_all()
