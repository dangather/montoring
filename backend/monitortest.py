import os
from time import perf_counter as pc, sleep
from dotenv import load_dotenv
load_dotenv()
from threading import Thread
import json
import subprocess as sp
from supabase import create_client
from datetime import datetime, timedelta
from colorama import init, Fore, Back, Style
import random

init()

# ========= important variables =========
url = os.environ.get("URL")
key = os.environ.get("KEY")
sb = create_client(url, key)
s = sb.table("schedule")
'''
FIELDS
id
name
scheduled_time
expected_elapsed
command
interval
pass_condition
'''


l = sb.table("logs")
'''
FIELDS
created_at (aka time of log)
command
result
advice
'''

# ========= log types =========

# positive logs
def plog(s):
    print(f"{Fore.GREEN}[+] [{datetime.now()}]{Style.RESET_ALL} {s}")

# negative logs
def nlog(s):
    print(f"{Fore.RED}[-] [{datetime.now()}]{Style.RESET_ALL} {s}")

# mid logs
def mlog(s):
    print(f"{Fore.YELLOW}[~] [{datetime.now()}]{Style.RESET_ALL} {s}")    

# custom log
def clog(i, s):
    return f"{Fore.MAGENTA}[{i}]{Style.RESET_ALL} {s}"

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
        # flag = not flag if random.randint(1, 10) > 5 else flag
        if flag:
            plog(clog(self.name, f"success operation finished in {elapsed}s"))
            update("schedule", "result", "success", "name", self.name)
            success = True
        else:
            nlog(clog(self.name, f"failure: {d}, operation finished in {elapsed}s"))
            update("schedule", "result", "failure", "name", self.name)
            log(self.name, "failure", "none")
            success = False
        if elapsed < ee:
            plog(clog(self.name, f"finished {ee-elapsed}s earlier than expected"))
        elif elapsed > ee:
            nlog(clog(self.name, f"finished {elapsed-ee}s later than expected."))
        else:
            mlog(clog(self.name, f"finished on time"))

        updateschedule(int(getdata(s, "interval", "command", command)), int(getdata(s, "id", "command", command)))




def update(table, selector, query, where, what):
    try:
        sb.table(table).update({selector: str(query)}).eq(where, what).execute()
    except json.decoder.JSONDecodeError:
        plog(clog(getdata(s, "name", where, what), f"updated {selector} with query {query} on {table} where {where} is {what}"))
    except Exception as e:
        nlog(f"an error occured: {e}")   

# update schedule
# i is interval
# r is id to update
def updateschedule(i, r):
    try:
        plog(clog(getdata(s, "name", "id", r), "currently updating schedule"))
        sb.table("schedule").update({"scheduled_time": str(datetime.strftime(datetime.now() + timedelta(seconds=i), "%H:%M:%S"))}).eq("id", r).execute()
    # json decode means server is up
    except json.decoder.JSONDecodeError:
        plog(clog(getdata(s, "name", "id", r), f"added {i} seconds to schedule"))
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
    threads = []
    for i in range(len(scope)):
        thread = Thread(target=threadrun, args=[scope[i]])
        threads.append(thread)
    for i in threads:
        i.start()

def threadrun(scope):
    try:
        sb.table("schedule").update({"scheduled_time": str(datetime.strftime(datetime.now() + timedelta(seconds=5), "%H:%M:%S"))}).eq("command", scope).execute()
    except json.decoder.JSONDecodeError:
        time = getdata(s, "scheduled_time", "command", scope)
        while True:
            now = datetime.now().strftime("%H:%M:%S")
            if now == time:
                task = Task(getdata(s, "name", "command", scope), getdata(s, "expected_elapsed", "command", scope))
                task.run(scope, getdata(s, "pass_condition", "command", scope))
                time = getdata(s, "scheduled_time", "command", scope)
            else:
                sleep(1)
    except KeyboardInterrupt:
        exit()

def getcommands():
    commands = fetch(s, "command") # fetch commands
    global tasks
    tasks = []
    for i in commands:
        tasks.append(i["command"])
    taskssplit = []
    split = 2
    for i in range(0, len(tasks), split):
        taskssplit.append(tasks[i:(i+split)])
    return taskssplit

def log(name, result, advice):
    try:
        l.insert({"name": name, "result": result, "advice": advice}).execute()
    except json.decoder.JSONDecodeError:
        pass

# TODO optimize these threads

# main
def main():
    try:
        mlog("starting the monitoring system...")
        taskssplit = getcommands()

        # start threads
        threads = []
        for i in range(len(taskssplit)):
            thread = Thread(target=t1, args=[taskssplit[i]])
            threads.append(thread)
        for i in threads:
            i.start()
        mlog("monitoring...")
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(f"there was an error: {e}")
        
if __name__ == "__main__":
    main()
