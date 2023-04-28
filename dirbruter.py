# 爆破首层目录 
import queue
import requests
import threading
import sys

class dirbruter():
    def __init__(self, target) -> None:
        self.target = target

    # 最终生成一个words队列 
    def get_words(self, resume=None):
        EXTENSIONS = ['.php', '.bak', '.orig', '.inc']
        WORDLIST = "./resources/gobuster_dictionary_common.txt"

        # 在words队列中扩充：不带后缀的文件&文件夹&带后缀的文件
        def extend_words(word):
            if "." in word:
                words.put(f'/{word}')
            else:
                words.put(f'/{word}/')
            for extension in EXTENSIONS:
                words.put(f'/{word}{extension}')

        words = queue.Queue()
        with open(WORDLIST, 'r') as t:
            lines = t.readlines()
        resume_flag = False
        for word in lines:
            word = word.strip('\n')
            if resume is not None:
                if resume_flag:
                    extend_words(word)
                elif word == resume:
                    resume_flag = True
                    print(f"[*] Find resume: {resume}")
            else:
                extend_words(word)

        return words


    def run(self, words):
        headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"}
        while not words.empty():
            url = f'{self.target}{words.get()}'
            try:
                response = requests.get(url, headers=headers)
            except requests.exceptions.ConnectionError:
                sys.stderr.write('x')
                sys.stderr.flush()
            else:
                if response.status_code == 200:
                    print(f'\n[^_^] Found: {url}')
                elif response.status_code == 404:
                    sys.stderr.write('.')
                    sys.stderr.flush()
                else:
                    print(f'\n[ToT] {response.status_code} : {url}')



if __name__ == '__main__':
    try:
        mydirbruter = dirbruter(sys.argv[1])
        words = mydirbruter.get_words()
        threads = []
        for i in range(50):
            new_thread = threading.Thread(target=mydirbruter.run, args=(words,))
            new_thread.start()
            threads.append(new_thread)
        for thread in threads:
            thread.join()
    except:
        print("Usage: python dirbruter.py [your_target]")
        sys.exit()






