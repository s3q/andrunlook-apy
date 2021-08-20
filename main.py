import sys
import os
import subprocess
import requests
import andr
import timeago
import datetime
from time import sleep

api = andr.api()

adb_dir = andr.set_adb_dir()

aid = andr.get_aid()


def options():
    pin = {
        "_id": "",
        "pin_range": [],
        "pin_list": [],
        "embedded_numbers": [],
        "pin_public": False,
        "pin_length": 0,
        "name": ""
    }
    o1 = int(input("""
[1] - try from public pin range
[2] - range of numbers
[3] - select your progress from database
[4] - start range from 0000
─── """).strip())
    if o1 == 1:
        pin_list = []
        pincp_list = api.getAllPublicProgress()
        pin["pin_public"] = True

        if pincp_list:
            for pincp in pincp_list:
                pin_list.append(pincp["pin"])
            pin["pin_list"] = pin_list

    elif o1 == 2:
        while True:
            o2 = input(
                "[-] - type tow numbers only with - for each it likely a pin will fall between them : \n─── ").strip()
            if len(o2.split("-")) == 2:
                pin["pin_range"] = list(map(int, o2.split("-")))
                pin["pin_length"] = len(str(pin["pin_range"][1]))

                if pin["pin_length"] < 4:
                    o3 = int(
                        input("[-] - type length for pin: \n─── ").strip())
                    if 4 <= o3 <= 8:
                        pin["pin_length"] = o3
                break
            else:
                print("[!] - please input tow numbers only !")
                continue

    elif o1 == 3:
        pin_progress = api.getAllProgress(aid)
        print(pin_progress)
        for index, pinp in enumerate(pin_progress):
            print(f"[{str(index)}] - " + pinp["name"] + " - " + pinp["device"] + " - " + pinp["createdAt"])

            if index == (len(pin_progress) - 1):
                while True:
                    o2 = int(input("[-] - type index to continue progress: \n─── ").strip())
                    if o2 > len(pin_progress) - 1:
                        print("[!] - please type valid index")
                        continue

                    pin["_id"] = pin_progress[o2]["_id"]
                    pin["pin_range"] = list(map(int, pin_progress[o2]["pinRange"]))
                    pin["pin_length"] = int(pin_progress[o2]["pinLength"])
                    pin["embedded_numbers"] = list(map(int, pin_progress[o2]["embeddedNumbers"]))

                    if pin_progress[o2]["pinPublicProgress"]:
                        pin_public_list = api.getAllPublicProgress()[pin_progress[o2]["pinPublicProgress"]+1:]
                        pin["pin_list"] = pin_public_list

                    break

    elif o1 == 4:
        while True:
            o2 = int(input("[-] - type length for pin: \n─── ").strip())
            if 4 <= o2 <= 8:
                pin["pin_length"] = o2
                break
            else:
                print("[!] - please type valid length")
                continue
        pin["pin_range"] = [0000, pow(10, pin["pin_length"]) - 1]

    if o1 == 4 or o1 == 2:

        while True:
            o3 = input("[-] - type name for this progress : \n─── ").strip()

            if len(o3) > 25:
                print("[!] - please write small name : less than 24 character")
                continue
            elif not o3 or len(o3) < 1:
                print("[!] - you cant continue without specific progress name")
                continue

            pin["name"] = o3
            break

        o2 = input("[-] - type numbers with , for each it : \n─── ").strip()
        if o2:
            pin["embedded_numbers"] = list(map(int, o2.split(",")))


    print("[+] - pin options : ", pin)
    return pin


def exe(epin, pin_length, embedded_numbers=[]):
    pin_str = str(epin).zfill(pin_length)

    includes_embedded_numbers = False
    if embedded_numbers:
        for enum in embedded_numbers:
            if pin_str.find(str(enum)) >= 0:
                includes_embedded_numbers = True
    else:
        includes_embedded_numbers = True

    if includes_embedded_numbers:
        command = adb_dir+"adb.exe shell locksettings clear --old "+pin_str
        result = subprocess.run(command, capture_output=True, shell=True)
        # command = adb_dir+"adb.exe shell locksettings clear --old "+pin_str
        # with open("result.txt", "a") as f:
        #     f.write(command+"\n")
        return result
# returncode
# stdout


def sleep_exe(i):
    if i == 4 or i == 9:
        print("[+] - wait 30 second ...")
        sleep(30)
    elif i > 9:

        if i > 40:
            print("[+] - wait 60 second ...")
            sleep(60)
        else:
            print("[+] - wait 30 second ...")
            sleep(30)


def main():

    pin = options()
    try:

        print("[+] - Please wait " + str(int(((pow(10, pin["pin_length"])-41)
            * 60) / 60 / 60)) + " hours maximum for guess password ... ¬_¬")
        print("[+] - if you need for stop it press ctrl+c and your progress will saved in database ^_~")

        i = 0

        if pin["pin_range"]:
            #     plu = pin["pin_length"]
            #     for i in range(1, 5):
            #         for pl in range(4, pin["pin_length"]+1):
            #             if not plu <= pl:
            #                 for ip in range(pin["pin_range"][0], pow(10, pl)):
            #                     if ip > pin["pin_range"][1]:
            #                         break
            #                     exe(ip, plu, pin["embedded_numbers"])
            #         pl -= 1

            for pl in range(4, pin["pin_length"]+1):
                for ip in range(pin["pin_range"][0], pow(10, pl)):
                    if ip > pin["pin_range"][1]:
                        break
                    pin["pin_list"].append(ip)
     
        if pin["pin_list"]:
            for p in pin["pin_list"]:
                result = exe(p, len(str(p)), pin["embedded_numbers"])
                # print(result)
                # print(result.stdout.decode().strip(), result.returncode, result.stderr.decode().strip())
                if result.returncode:
                    print("[!] -", result.stderr.decode().strip())
                    print("[-] - please check if device is connectd and try agin ... >_<")
                    exit()

                if result.stdout.decode().strip().find("user has no password") >= 0:
                    print("[!] -",result.stdout.decode().strip())
                    exit()
                elif result.stdout.decode().strip().find("Lock credential cleared") >= 0:
                    print("[+] - we find find your pin ^_____^", p)
                    api.savePublicProgress(aid, p)
                    exit()

                # no devices/emulators found
                # didn't match
                # Lock credential cleared
                # user has no password

                pin["pin"] = p
                sleep_exe(i)
                i += 1
    except KeyboardInterrupt: 
        if i != 0 and pin:
            if pin["pin_public"]:
                api.saveProgress(aid, pin["name"], pin["_id"], i, [], pin["embedded_numbers"], pin["pin_length"])
                print("[+] - your porgress was saved successfully ")
            elif pin["pin_range"]:
                api.saveProgress(aid, pin["name"], pin["_id"], 0, [pin["pin"], pin["pin_range"][1]], pin["embedded_numbers"], pin["pin_length"])
                print("[+] - your porgress was saved successfully ")

        
        print(pin)
        exit()

    print("[!] - sorry we didn't found you pin ... please try with another way")


    # for i in range(pin[])
main()
