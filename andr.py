import requests
import os
import sys
import uuid


class api:

    def __init__(self):
        self.API = "http://localhost:8800/"

    def savePublicProgress(self, aid, pin):
        try:
            data = {"aid": aid, "pin": pin}
            req = requests.post(f"{self.API}api/andrpublicprogress", data)
            return req.json()

        except:
            return None

    def getAllPublicProgress(self):
        try:
            req = requests.get(f"{self.API}api/andrpublicprogress/all")
            return req.json()
        except:
            return None

    def saveProgress(self, aid, name, _id="", pinPublicProgress=0, pinRange=[], embeddedNumbers=[], pinLength=0):
        try:
            data = {"aid": aid, "name": name, "_id": _id, "pinPublicProgress": pinPublicProgress, "pinRange": pinRange,
                    "embeddedNumbers": embeddedNumbers, "pinLength": pinLength}        
            req = requests.post(f"{self.API}api/andrprogress", data)
            return req.json()

        except:
            return None

    def deleteProgress(self, aid, _id):
        try:
            req = requests.delete(
                f"{self.API}api/andrprogress/{aid}/{_id}")
            return req.json()
        except:
            return None

    def deleteAllProgress(self, aid):
        try:
            req = requests.delete(f"{self.API}api/andrprogress/all/{aid}")
            return req.json()
        except:
            return None

    def getProgress(self, aid, _id):
        try:
            req = requests.get(
                f"{self.API}api/andrprogress/{aid}/{_id}")
            return req.json()
        except:
            return None

    def getAllProgress(self, aid):
        try:
            req = requests.get(f"{self.API}api/andrprogress/all/{aid}")
            return req.json()
        except:
            return None


def set_adb_dir():
    platform = sys.platform.lower()
    if platform.startswith("win"):
        return "windows\\"
    elif platform.startswith("linux") or platform.startswith("mac"):
        return "linux/"
    else:
        print("[!] - Don't support you os")
        os.system("pause")
        exit()


def generate_aid():
    if not os.path.isfile("andrDB.txt"):
        with open("andrDB.txt", "w") as f:
            f.write(str(uuid.uuid4()))


def get_aid():
    generate_aid()
    with open("andrDB.txt", "r") as f:
        return f.read()
