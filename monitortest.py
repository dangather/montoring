import os
from time import perf_counter as pc, sleep
from dotenv import load_dotenv
load_dotenv()
from threading import Thread
import json
import subprocess as sp
from supabase import create_client
from datetime import datetime, timedelta

# important variables
url = os.environ.get("URL")
key = os.environ.get("KEY")
sb = create_client(url, key)
s = sb.table("schedule")
l = sb.table("logs")
# ========= log types =========

# positive logs
def plog(s):
    print(f"[+] [{datetime.now()}] {s}")

# negative logs
def nlog(s):
    print(f"[-] [{datetime.now()}] {s}")

# mid logs
def mlog(s):
    print(f"[~] [{datetime.now()}] {s}")    

# custom log
def clog(i, s):
    return f"[{i}] {s}"

# ========= Task class =========

class Task:
    # class init
    def __init__(self, name, expected_elapsed):
        self.name = name
        self.expected_elapsed = expected_elapsed
    
    # run command
    def run(self, command, condition):
        # vars init
        plog(clog(self.name, f"running..."))
        c = command
        ee = self.expected_elapsed
        now = pc()
        d = sp.Popen(c, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT).stdout.readlines() # runs command on machine
        after = pc()

        # calculating elapsed time for command run
        elapsed = int(after - now)
        round(float(ee),3)
        round(elapsed,3)

        # parsing output
        for i,e in enumerate(d):
            d[i] = e.decode("utf-8")
        # checking pass condition
        for i in d:
            if condition in i:
                flag = True
                break
            else:
                flag = False
        # log output
        if flag:
            plog(clog(self.name, f"success operation finished in {elapsed}s"))
        else:
            nlog(clog(self.name, f"failure: {d}, operation finished in {elapsed}s"))
        if elapsed < ee:
            plog(clog(self.name, f"finished {ee-elapsed}s earlier than expected"))
        elif elapsed > ee:
            nlog(clog(self.name, f"finished {elapsed-ee}s later than expected."))
        else:
            mlog(clog(self.name, f"finished on time"))

# update schedule
# i is interval
# r is id to update
def updateschedule(i, r):
    try:
        plog(clog(getdata(s, "name", "id", r), "currently updating schedule"))
        sb.table("schedule").update({"scheduled_time": str(datetime.strftime(datetime.now() + timedelta(minutes=i), "%H:%M:%S"))}).eq("id", r).execute()
    # json decode means server is up
    except json.decoder.JSONDecodeError:
        plog(clog(getdata(s, "name", "id", r), f"added {i} minutes to schedule"))
        plog(clog(getdata(s, "name", "id", r), "updated schedule"))
        sleep(0.5)
    except Exception as e:
        nlog(f"an error occured: {e}")

# get general data
def fetch(table, selector):
    data = json.loads(table.select(selector).order("id").execute().json())["data"]
    return data

# get specific data using specific filters
def getdata(table, selector, what, where):
    return json.loads(table.select(selector).eq(what, where).execute().json())["data"][0][selector]

# thread 1 - first two commands
def t1(scope):
    print(scope)
    for f in range(len(scope)):
        task = Task(getdata(s, "name", "command", scope[f]), getdata(s, "expected_elapsed", "command", scope[f]))
        task.run(scope[f], getdata(s, "pass_condition", "command", scope[f]))
        updateschedule(int(getdata(s, "interval", "command", scope[f])), int(getdata(s, "id", "command", scope[f])))

# main
def main():
    mlog("starting the monitoring system...")
    commands = fetch(s, "command") # fetch commands
    global tasks
    tasks = []
    for i in commands:
        tasks.append(i["command"])
    taskssplit = []
    split = 2
    for i in range(0, len(tasks), split):
        taskssplit.append(tasks[i:(i+split)])
    
    # start threads
    threads = []

    for i in range(len(taskssplit)):
        thread = Thread(target=t1, args=[taskssplit[i]])
        threads.append(thread)
    print(threads)
    for i in threads:
        i.start()

if __name__ == "__main__":
    main()
