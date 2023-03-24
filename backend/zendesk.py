import os
from zenpy import Zenpy
from dotenv import load_dotenv
load_dotenv()


def gettickets():
    for ticket in client.users():
        print(ticket)


def main():
    creds = {
        "email": str(os.environ.get("ZENMAIL")),
        "password": str(os.environ.get("ZENPWD")),
        "subdomain": "gathertech"
    }
    print(creds)
    global client
    client = Zenpy(**creds)

    gettickets()

if __name__ == "__main__":
    main()