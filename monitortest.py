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
    print(f"[+] {s}")


def nlog(s):
    print(f"[-] {s}")


class test:
    def __init__(self, name, time, expected_elapsed):
        self.name = name
        self.time = time
        self.expected_elapsed = expected_elapsed
    
    def run(self, c, ee, condition):
        print(f"[+] running {self.name}...")
        now = pc()
        d = sp.Popen(c, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT).stdout.readlines()
        after = pc()
        elapsed = int(after - now)
        round(float(ee),3)
        round(elapsed,3)
        print(f"[+] done! operation finished in {elapsed}s")
        for i,e in enumerate(d):
            d[i] = e.decode("utf-8")
        for i in d:
            if condition in i:
                flag = True
                break
            else:
                flag = False
        if flag:
            plog("success!")
        else:
            nlog(f"failure: {d}")
        if elapsed < ee:
            print(f"[+] finished {ee-elapsed}s earlier than expected!")
        elif elapsed > ee:
            print(f"[-] finished {elapsed-ee}s later than expected.")
        else:
            print(f"[+] finished on time!")

def updateschedule():
    updatedtime = str(datetime.strftime(datetime.now()+timedelta(seconds=10), "%H:%M:%S"))
    try:
        sb.table("schedule").update({"scheduled_time": updatedtime}).eq("id", 1).execute()
        sleep(0.5)
    except json.decoder.JSONDecodeError:
        plog("updated schedule!")
    except:
        nlog("an error occured")

def fetch(selector, i, specific):
    data = json.loads(s.select(selector).execute().json())["data"][i][specific]
    return data

def main():
    plog("starting up monitoring system")
    time = datetime.strptime(json.loads(s.select("scheduled_time").execute().json())["data"][0]["scheduled_time"], "%H:%M:%S").time()
    while True:
        current = datetime.now().strftime("%H:%M:%S")
        print(current, time)
        if str(current) == str(time):
            tests = []
            idd = []
          
            for i in json.loads(s.select("id").execute().json())["data"]:
                idd.append(i["id"])
            
            expected_elapsed = json.loads(s.select("expected_elapsed").execute().json())["data"][0]["expected_elapsed"]
            ping = test("ping", time,expected_elapsed)
            tests.append([time, expected_elapsed])
            ping.run(json.loads(s.select("command").execute().json())["data"][0]["command"], expected_elapsed, "Reply")
            updateschedule()
            time = datetime.strptime(json.loads(s.select("scheduled_time").execute().json())["data"][0]["scheduled_time"], "%H:%M:%S").time()
        sleep(1)
        



if __name__ == "__main__":
    print(fetch("command", 0, "command"))
