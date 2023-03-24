from monitortest import *

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
