
def get_all():
	all_list = list()
	all_list.append("https://status.github.com/messages")
	all_list.append("https%3A%2F%2Fstatus.github.com")
	
	all_list = [(item, "Open Redirect") for item in all_list]
	return all_list

def checkSuccess(content):
	# print(len(content.history), content.url)
	if len(content.history) > 0 and content.url == "https://status.github.com/messages":
		return True
	return False


if __name__ == "__main__":	
	print	get_all()
