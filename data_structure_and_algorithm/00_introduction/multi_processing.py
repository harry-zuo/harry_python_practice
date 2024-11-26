import os
import time
import random

def long_time_task(name):
    print(f'Run task {name}(pid:{os.getpid()}) ...')
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print(f'Finish {name}(pid:{os.getpid()}) task with {(end - start):.1f} ...')
