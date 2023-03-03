import os
from time import perf_counter as pc, sleep
from dotenv import load_dotenv
load_dotenv()
from threading import Thread
import json
import subprocess as sp
from supabase import create_client
from datetime import datetime, timedelta

url = os.environ.get("URL")
key = os.environ.get("KEY")
sb = create_client(url, key)
s = sb.table("schedule")

def plog(s):
    print(f"[+] [{datetime.now()}] {s}")


def nlog(s):
    print(f"[-] [{datetime.now()}] {s}")


class Task:
    def __init__(self, name, expected_elapsed):
        self.name = name
        self.expected_elapsed = expected_elapsed
    
    def run(self, command, condition):
        plog(f"running {self.name}...")
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
            plog(f"success operation finished in {elapsed}s")
        else:
            nlog(f"failure: {d}, operation finished in {elapsed}s")
        if elapsed < ee:
            plog(f"finished {ee-elapsed}s earlier than expected")
        elif elapsed > ee:
            nlog(f"finished {elapsed-ee}s later than expected.")
        else:
            plog(f"finished on time")

def updateschedule(i, r):
    try:
        sb.table("schedule").update({"scheduled_time": str(datetime.strftime(datetime.now() + timedelta(minutes=i), "%H:%M:%S"))}).eq("id", r).execute()
    except json.decoder.JSONDecodeError:
        plog(f"added {i} minutes to {r}")
        plog("updated schedule")
        sleep(0.5)
    except Exception as e:
        nlog(f"an error occured: {e}")

def fetch(selector):
    data = json.loads(s.select(selector).order("id").execute().json())["data"]
    return data

def getdata(selector, what, where):
    return json.loads(s.select(selector).eq(what, where).execute().json())["data"][0][selector]

def t1():
    scope = tasks if len(tasks) <= 2 else tasks[:2]
    for f in range(len(scope)):
        task = Task(getdata("name", "command", scope[f]), getdata("expected_elapsed", "command", scope[f]))
        task.run(getdata("command", "command", scope[f]), getdata("pass_condition", "command", scope[f]))
        updateschedule(int(getdata("interval", "command", scope[f])), f)
  
def main():
    plog("starting the monitoring system...")
    commands = fetch("command")
    global tasks
    tasks = []
    for i in commands:
        tasks.append(i["command"])
    t1()


if __name__ == "__main__":
    main()
