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


def updateJson(file, updated_data):
    data = readJson(file)
    #data.update(new_data)
    for server in data["servers"]:
            server["status"] = updated_data
            server["last_checked"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(file, 'w') as outfile:
        json.dump(data, outfile, indent=4, separators=(',',': '))


def check(file):
    while True:
        data = readJson(file)
        for server in data["servers"]:
            updateJson(file, myping(server["host"], server["ip"]))
        time.sleep(120)








if len(sys.argv) < 2:
    print("Usage: python script_name.py [COMMAND] [ARGUMENTS]")
    print("Commands:")
    print("  add HOST IP FILE        Add a server to the file")
    print("  remove HOST FILE        Remove a server from the file")
    print("  show FILE               Show all servers in the file")
else:
    command = sys.argv[1]
    if command == "add":
        if len(sys.argv) < 5:
            print("Usage: python script_name.py add HOST IP FILE")
        else:
            host = sys.argv[2]
            ip = sys.argv[3]
            file = sys.argv[4]
            AddServer(host, ip, file)
    elif command == "remove":
        if len(sys.argv) < 4:
            print("Usage: python script_name.py remove HOST FILE")
        else:
            host = sys.argv[2]
            file = sys.argv[3]
            RemoveServer(host, file)
    elif command == "show":
        if len(sys.argv) < 3:
            print("Usage: python script_name.py show FILE")
        else:
            file = sys.argv[2]
            showServers(file)
    else:
        print("Unknown command:", command)
        
#AddServer("www.udemy.com", "15.20.45.82", "servers.json")

#showServers("servers.json")

#RemoveServer("www.udemy.com", "servers.json")

#check("servers.json")

def main():
    modus = input("Kies tussen Management modus en check modus \nDruk op 1 om management modus te starten \nDruk op 2 om check modus te starten ")
    if modus == "1":
        print()
        vraag = input("Druk op 1 om alle servers te tonen\nDruk op 2 om een server toe te voegen\nDruk op 3 om een server te verwijderen ")
        if vraag == "1":
            showServers("servers.json")
        elif vraag == "2":
            host = input("Geef de host naam in ")
            ip = input("Geef de host naam in ")
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