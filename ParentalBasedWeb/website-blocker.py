import time
import sqlite3 as db
from datetime import datetime as dt

con = db.connect("parentsdb.db")

with con:
    

#hostsPath="hosts"
    hostsPath="C:\Windows\System32\drivers\etc\hosts"
    redirect="127.0.0.1"
    cur = con.cursor()
    phone_number = int(input("Enter phone numer :"))
    web = ('SELECT websites FROM parents WHERE phone_no = ?')
    cur.execute(web,[(phone_number)])
    websites = cur.fetchone()
    
    while True:
        if dt(dt.now().year,dt.now().month,dt.now().day,8) < dt.now() < dt(dt.now().year,dt.now().month,dt.now().day,22):
            print ("Working hours...")
            with open(hostsPath,'r+') as file:
                content=file.read()
                for site in websites:
                    if site in content:
                        pass
                    else:
                        file.write(redirect+" "+site+"\n")
        else:
            with open(hostsPath,'r+') as file:
                content=file.readlines()
                file.seek(0)
                for line in content:
                    if not any(site in line for site in websites):
                        file.write(line)
                file.truncate()
            print ("Fun hours...")
        time.sleep(5)

