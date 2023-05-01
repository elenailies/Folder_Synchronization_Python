import os
import hashlib
import time
import shutil
# import atexit
import sys


# function to write message in the log file
def log(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(log_file, 'a') as f:
        f.write('[' + current_time + ']' + message + '\n')


# @atexit.register
# def on_close():
#     log('Session ended')


##############################################################################

# function to compare two files
def compare_files(file1, file2):
    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            if hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest():
                return True
            else:
                return False


###############################################################################################

# function to sync two folders
def synchronization(source, replica):

    source_files = os.listdir(source)
    replica_files = os.listdir(replica)

    for filename in source_files:
        source_path = os.path.join(source, filename)
        replica_path = os.path.join(replica, filename)

        if os.path.isfile(source_path):
            # Verifies if a file from the source folder is in the replica folder
            # and updates the contents if it is found but the contents are different.
            if filename in replica_files:
                if not compare_files(source_path, replica_path):
                    shutil.copyfile(source_path, replica_path)
                    log(f'file {filename} is copied')
                    print(f'file {filename} is copied')
            # If the file is in the source folder but not in the replica folder,
            # the file will be copied in the replica folder.
            if filename not in replica_files:
                shutil.copyfile(source_path, replica_path)
                log(f'file {filename} is created')
                print(f'file {filename} is created')

        elif os.path.isdir(source_path):
            # If the directory is in the source folder but not in the replica folder,
            # the directory will be created in the replica folder.
            if not os.path.exists(replica_path):
                os.makedirs(replica_path)
                log(f'directory {filename} is created')
                print(f'directory {filename} is created')
            synchronization(source_path, replica_path)

    for filename in replica_files:
        replica_path = os.path.join(replica, filename)
        # If the file is in the replica folder but not in the source folder,
        # the file will be deleted from the replica folder.
        if os.path.isfile(replica_path) and filename not in source_files:
            os.remove(replica_path)
            log(f'file {filename} is deleted')
            print(f'file {filename} is deleted')
        # If the directory is in the replica folder but not in the source folder,
        # the directory will be deleted from the replica folder.
        elif os.path.isdir(replica_path) and filename not in source_files:
            shutil.rmtree(replica_path)
            log(f'directory {filename} is deleted')
            print(f'directory {filename} is deleted')


##############################################################################
# Folder paths, synchronization interval and log file path are provided
# using the command line arguments
args = sys.argv
folder = args[1]
backup = args[2]
interval = int(args[3])
log_file = args[4]

sync = True
if not os.path.exists(folder):
    print("Source folder does not exist")
    sync = False
if not os.path.exists(backup):
    print("Replica folder does not exist")
    sync = False
if not os.path.exists(log_file):
    print("Log file does not exist")
    sync = False

# log_file = 'log.txt'
# folder = r'C:\Users\user\PycharmProjects\pythonProject\Source'
# backup = r'C:\Users\user\PycharmProjects\pythonProject\Replica'
# interval = 120

##############################################################################

log('Start session')

# do synchronization every interval
while True:

    if sync:
        synchronization(folder, backup)
        time.sleep(interval)
