
def get_all():
	all_list = list()
	all_list.append("https://status.github.com/messages")
	all_list.append("https%3A%2F%2Fstatus.github.com")
	
	all_list = [(item, "Open Redirect") for item in all_list]
	return all_list


if __name__ == "__main__":	
	print	get_all()
