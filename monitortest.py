import os
from time import perf_counter as pc
from dotenv import load_dotenv
load_dotenv()
from threading import Thread
import json
import subprocess as sp
from supabase import create_client, Client
from datetime import datetime

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
        s = []
        for i in d:
            s.append(i.decode("utf-8"))
        if condition in d:
            plog("success!")
        else:
            nlog("failure.")
            print(d)

        if elapsed < ee:
            print(f"[+] finished {ee-elapsed}s earlier than expected!")
        elif elapsed > ee:
            print(f"[-] finished {elapsed-ee}s later than expected.")
        else:
            print(f"[+] finished on time!")

command = "ping 212.188.157.218 /n 1"

name = json.loads(s.select("name").execute().json())["data"][0]["name"]
time = s.select("scheduled_time").execute()
expected_elapsed = json.loads(s.select("expected_elapsed").execute().json())["data"][0]["expected_elapsed"]

ping = test(name,time,expected_elapsed)
ping.run(command, expected_elapsed, "Reply")


