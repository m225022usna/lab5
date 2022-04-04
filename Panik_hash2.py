#!/usr/bin/python3
#Lab 5 Example

import os
import sys
import hashlib
import datetime

new=[]
missing=[]
modified=[]
old_files={}
new_files={}

ignore_list = ['dev', "proc", "run", "sys", "tmp", "var/lib", "var/run",".wine"]
now = datetime.datetime.now()

def main():
   for root, dirs, files in os.walk("/home/sy402/Desktop", topdown=True): #from geeksforgeeks.org

     for item in ignore_list:
            if item in dirs:
                dirs.remove(item)
     testlist = root.split("/")
     gethashes = open("hashit.mtd", "r")
     gethashes = gethashes.readlines()
     for line in gethashes:
         filename=line.split(",")[0]
         filehash =line.split(",")[2].rstrip("\n")
         old_files[filename]=filehash
     for directory in testlist:
         if (directory in ignore_list) and (directory in root.split()):
             continue

         else:
             for f in files:
                 current_file = os.path.join(root,f)

                 if current_file not in old_files:
                     print("New File: ", current_file)
                 H = hashlib.sha256()
                 try:
                     with open(current_file, "rb") as FIN:
                         H.update(FIN.read())
                         hash = H.hexdigest()
                         new_files[current_file]=hash
                         if old_files[current_file]!=hash:
                             print("File Changed: ", current_file)
                        ### Mostly taken from stackoverflow ; strftime is from W3schools###
                         with open("hashit.mtd", "a+") as myfile:
                             myfile.write(current_file),myfile.write(","),myfile.write(now.strftime("%Y-%m-%d %H:%M:%S")),myfile.write(","),myfile.write(H.hexdigest()),myfile.write("\n")

                 except:
                     print(current_file)

def compare():
    for file in old_files:
        if file not in new_files:
            print("File missing: ", file)
            print("\n\n"+old_files+"\n\n")


if __name__ == "__main__":
   main()
   compare()