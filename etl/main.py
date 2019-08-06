import subprocess
import sys
from multiprocessing import Pool
from etl.callbacks import *



def create(sub):
    subprocess.run(sub, stdout=sys.stdout)



if __name__ == '__main__':
    sub_processes = [["python", "load_buckets.py"], ["python", "load_oracle.py"]]
    processes = Pool()

    for sp in sub_processes:
        processes.apply_async(func=create, args=(sp,), callback=done, error_callback=error)

    processes.close()
    processes.join()
