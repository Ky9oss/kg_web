import contextlib
import os
import queue
import time
import requests
import sys
import threading 


RUBBED = "/home/kadrex/Study/blog/public/"
FILTERED = [".jpg", ".git", ".png", ".css", ".scss"]
THREADS = 10
TARGET = "https://ky9oss.top"
paths_queue = queue.Queue()
answers = queue.Queue()

def rubbing_here():
    for here, _, filenames in os.walk("."):
        for filename in filenames:
            if os.path.splitext(filename)[1] in FILTERED:
                continue
            path = os.path.join(here, filename)
            if path.startswith("."):
                path = path[1:]
            paths_queue.put(path)
            print(path)


# 快捷创建上下文管理器
@contextlib.contextmanager
def chdir(path):
    this_dir = os.getcwd()

    # __enter__
    os.chdir(path)

    try:
        yield
    finally:
        # __exit__
        os.chdir(this_dir)

def hack_remote():
    while not paths_queue.empty():
        path = paths_queue.get()
        url = f'{TARGET}{path}'
        time.sleep(2)
        r = requests.get(url)
        if r.status_code == 200:
            answers.put(url)
            sys.stdout.write('+')
        else:
            sys.stdout.write('x')


def run():
    threads = []
    for i in range(THREADS):
        print(f'thread{i}')
        mythread = threading.Thread(target=hack_remote)
        mythread.start()
        threads.append(mythread)
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    with chdir(RUBBED):
        rubbing_here()
    input("Press return to continue")
    run()
    with open('answers.txt', 'w') as f:
        while not answers.empty():
            f.write(f'{answers.get()}\n')
    print("DONE")


