#!/usr/bin/python3 -B

# Import the required libraries
import os, sys, hashlib, time

# Away to automatically abort unhandleable files...
import signal

class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm

# Get the root of the filesystem to scan from the command line
if len(sys.argv) < 2:
    print('Please provide the root of the directory structure to scan as an argument!')
    sys.exit()
BASEDIR = sys.argv[-1]

# Ignorable Directories and Files
IGNORE_DIR = ['/dev', '/proc', '/run', '/sys', '/tmp','/var/lib', '/var/run']
IGNORE_FILE = ['../J-01.So Much Data/notes.txt']

'''
Retrieve stored metadata
'''
def load_metadata(filename='hashit.mtd'):
    try:
        results = open(filename,'r').readlines()
        results = eval(results[0])
        return results[0], results[1]
    except:
        return {}, {}

'''
Save metadata
'''
def save_metadata(FDB, HDB, filename='hashit.mtd'):
    try:
        results = open(filename, 'w')
        results.write(str([FDB,HDB])+'\n')
        results.close()
    except:
        pass

'''
Hash the files
'''
def hashit(filename):
    BUFFER_SIZE = 65536
    sha256 = hashlib.sha256()
    try:
        # Break the try/except after 2 seconds if the hash continues
        # I am impatient...
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(2)
        with open(filename, 'rb') as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                sha256.update(data)
        signal.alarm(0)
    except IOError:
        pass
    except Alarm:
        print('I\'m bored, moving on...')
    return sha256.hexdigest()

# Store the information in a way that we can work with it later.
FDB, HDB = load_metadata()

# Start the scan
for root, directory, files in os.walk(BASEDIR):
    PATH_OK = True
    for check in IGNORE_DIR:
        if check.find(root) == 0 or root.find(check) == 0:
            PATH_OK = False
    if PATH_OK:
        for file in files:
            this_file = root + '/' + file
            if this_file not in IGNORE_FILE:
                print(root)
                print(this_file)
                this_hash = hashit(this_file)
                print(this_hash)
                this_time = time.time()
                if this_file in FDB and FDB[this_file][0] != this_hash:
                    print('MODIFIED:'),
                    print(this_file)
                    print(this_hash)
                    print('LAST HASH TIME:'),
                    print(time.asctime(time.localtime(FDB[this_file][1])))
                FDB[this_file] = [this_hash, this_time]
                HDB[this_hash] = [this_file, this_time]

# Save the results
save_metadata(FDB, HDB)