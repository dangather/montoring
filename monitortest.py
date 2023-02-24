import os
from time import perf_counter as pc, sleep
from dotenv import load_dotenv
load_dotenv()
from threading import Thread
import json
import subprocess as sp
from supabase import create_client
from datetime import datetime, timedelta
from threads import *

url = os.environ.get("URL")
key = os.environ.get("KEY")
sb = create_client(url, key)
s = sb.table("schedule")

def plog(s):
    print(f"[+] [{datetime.now()}] {s}")


def nlog(s):
    print(f"[-] [{datetime.now()}] {s}")


class Task:

    running = False

    def __init__(self, name, expected_elapsed):
        self.name = name
        self.expected_elapsed = expected_elapsed
    
    def run(self, command, condition):
        print(f"[+] running {self.name}...")
        c = command
        ee = self.expected_elapsed
        now = pc()
        d = sp.Popen(c, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT).stdout.readlines()
        after = pc()
        elapsed = int(after - now)
        round(float(ee),3)
        round(elapsed,3)
        for i,e in enumerate(d):
            d[i] = e.decode("utf-8")
        for i in d:
            if condition in i:
                flag = True
                break
            else:
                flag = False
        if flag:
            plog(f"success! operation finished in {elapsed}s")
        else:
            nlog(f"failure: {d}, operation finished in {elapsed}s")
        if elapsed < ee:
            print(f"[+] finished {ee-elapsed}s earlier than expected!")
        elif elapsed > ee:
            print(f"[-] finished {elapsed-ee}s later than expected.")
        else:
            print(f"[+] finished on time!")

def updateschedule(i, r):
    try:
        sb.table("schedule").update({"scheduled_time": str(datetime.strftime(datetime.now() + timedelta(seconds=i), "%H:%M:%S"))}).eq("id",r).execute()
        sleep(0.5)
    except json.decoder.JSONDecodeError:
        plog("updated schedule!")
    except Exception as e:
        nlog(f"an error occured: {e}")

def sfetch(selector, i):
    data = json.loads(s.select(selector).execute().json())["data"][i][selector]
    return data

def fetch(selector):
    data = json.loads(s.select(selector).execute().json())["data"]
    return data

def main():
    plog("starting the monitoring system...")
    commands = fetch("command")
    tasks = []
    for i in commands:
        tasks.append(i["command"])
    print(tasks)
    f = 0
    while f < len(commands):
        task = Task(sfetch("name", f), sfetch("expected_elapsed", f))
        task.run(sfetch("command", f), sfetch("pass_condition", f))

        f+=1
        if f == len(commands):
            f = 0       


if __name__ == "__main__":
    main()