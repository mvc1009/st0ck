#!/usr/bin/python3

import sys, os
import sqlite3

print("[+] Hello Cara carbasso")
print("[+] Install1ng V1rUs3s to 0sk1Th3Sh1t")
os.system("touch furgo.db")
connection = sqlite3.connect("~/Desktop/MiPC/Matachana/furgo.db")
#connection = sqlite3.connect("/Users/oscar/Desktop/MI PC/MATACHANA/ DOTACIÓN FURGO/furgo.db")
cursor = connection.cursor()

sql_command = "CREATE TABLE stock ( id VARCHAR(30) PRIMARY KEY, count INTEGER, name VARCHAR(30));"

cursor.execute(sql_command) #Execute sql commands
connection.commit() #Commit changes to database
connection.close()

print("[!] Installation completed, exiting!")