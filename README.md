# Folder_Synchronization_Python
 A program that synchronizes two folders: source and replica. The  program should maintain a full, identical copy of source folder at replica folder.
 
- synchronization is one-way: after the synchronization content of the replica folder is modified to exactly match content of the source folder
- synchronization is performed periodically
- file creation/copying/removal operations are logged to a file and to the console output
- folder paths, synchronization interval and log file path are provided using the command line arguments

Command line arguments example:  python main.py Source Replica 120 log.txt


