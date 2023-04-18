import os
import sys
import json
import time
from datetime import datetime

def myping(host, ip):
    status = None
    response = os.system("ping -c 1 " + host)
    
    if response == 0:
        status = "Online"
    else:
        status = "Offline"

    return status
    #return {
          #  'host': host,
            #'ip': ip,
            #'status': status,
           # 'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #}
        
def readJson(file):
    with open(file, 'r') as fp:
        data = json.load(fp)
        return data

def writeToJson(file, new_data):
    data = readJson(file)
    data["servers"].append(new_data)
    with open(file, 'w') as outfile:
        json.dump(data, outfile, indent=4, separators=(',',': '))
    
def AddServer(host, ip, file):
    data = readJson(file)
    new_data = {
            'host': host,
            'ip': ip,
            'status': None,
            'last_checked': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    if host in str(data):
        print("It already exists. ")
    else:
        writeToJson(file, new_data)
            
def RemoveServer(host, file):        
    data = readJson(file)
    for server in data["servers"]:
        if server["host"] == host:
            data["servers"].remove(server)
            with open(file, 'w') as outfile:
                json.dump(data, outfile, indent=4, separators=(',',': '))

def showServers(file):
    data = readJson(file)
    for server in data["servers"]:
        print(server["host"], server["ip"], server["status"], server["last_checked"])


def updateJson(file, updated_data, index):
    data = readJson(file)
    #data.update(new_data)
    for server in data["servers"]:
            #server["status"] = updated_data
            #server["last_checked"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data["servers"][index]["status"] = updated_data
            data["servers"][index]["last_checked"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(file, 'w') as outfile:
        json.dump(data, outfile, indent=4, separators=(',',': '))

def check(file):
    while True:
        data = readJson(file)
        #for server in data["servers"]:
        for i, server in enumerate(data["servers"]):
            status = myping(server["host"], server["ip"])
            updateJson(file, status, i)
        time.sleep(120)



def main():
    if len(sys.argv) > 1:
        if len(sys.argv) < 2:
            print("Usage: python program.py [management|check]")
            sys.exit(1)

        mode = sys.argv[1]

        if mode == "management":
            if len(sys.argv) < 3:
                print("Usage: python program.py management [show|add|remove]")
                sys.exit(1)

            action = sys.argv[2]

            if action == "show":
                showServers("servers.json")
            elif action == "add":
                if len(sys.argv) != 5:
                    print("Usage: python program.py management add [host] [ip]")
                    sys.exit(1)

                host = sys.argv[3]
                ip = sys.argv[4]
                AddServer(host, ip, "servers.json")
                print("Server added successfully.")
            elif action == "remove":
                if len(sys.argv) != 4:
                    print("Usage: python program.py management remove [host]")
                    sys.exit(1)

                host = sys.argv[3]
                RemoveServer(host, "servers.json")
                print("Server removed successfully.")
            else:
                print("Invalid")
                sys.exit(1)

        elif mode == "check":
            check("servers.json")
        else:
            print("Invalid mode.")
            sys.exit(1)
            
    else:
        modus = input("Kies tussen Management modus en check modus \nDruk op 1 om management modus te starten \nDruk op 2 om check modus te starten ")
        if modus == "1":
            print()
            vraag = input("Druk op 1 om alle servers te tonen\nDruk op 2 om een server toe te voegen\nDruk op 3 om een server te verwijderen ")
            if vraag == "1":
                showServers("servers.json")
            elif vraag == "2":
                host = input("Geef de host naam in ")
                ip = input("Geef de ip naam in ")
                AddServer(host,ip,"servers.json")
                print("U hebt een server toegevoegd ")
            elif vraag == "3":
                host = input("Geef de host naam in ")
                RemoveServer(host, "servers.json")
            else:
                print("Kies tussen 1  tot 3  a.u.b.")
        elif modus == "2":
            print("Om de 2 minuten gaan we nu alle servers in onze database checken ")
            check("servers.json")

if __name__ == "__main__":
    main()





