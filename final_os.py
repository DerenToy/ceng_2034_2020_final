#!/usr/bin/python3

#Name and Surname : KIYMET DEREN TOY 
#Student ID : 170709012

import os
import requests
import time
import uuid
import hashlib
import multiprocessing
import threading

#Question 1
"""
def create_child_process():
	pid = os.fork()
	
	# pid is greater than 0 means parent process
	if (pid >0):
		print("Parent process id is:" , os.getpid())

	# pid is equal to 0 means child process
	elif (pid==0):
		print("Child process id is:" , os.getpid())

create_child_process()


#Question 2

url = ["http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg",
"http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"]


pid= os.fork()

if( pid==0):
	def download_file (url, file_name = None):
		r = requests.get(url, allow_redirects =True)
		file = file_name if file_name else str(uuid.uuid4())
		open(file, 'wb').write(r.content)
	for i in url:
		download_file(i)




#Question 3

def orphan():
	pid = os.fork()
			
	# pid is greater than 0 means parent process
	if (pid>0):
        #When I use the "wait()" method, parent process waits for child process to finish.
		os.wait()
		print("I am a Parent process and my id is" , os.getpid())
	# pid is equal to 0 means child process
	elif (pid==0):	
		print("I am a Child process and my id is:" , os.getpid())
		os._exit(0)
orphan()



"""
#Question 4

urls = ["http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg",
"http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"]

# I want to check the time
begin_time = time.time()

def downloadFile(url, files):
    r = requests.get(url, allow_redirects=True)
    file = str(uuid.uuid4())
    open(file, 'wb').write(r.content)
    files.append(file)


# To check child process is done
# I am using a flag
# This is a shared resource between processes
isDone = multiprocessing.Value('i',0)

# n is zero if we are in child process
# n is positive if we are in parent process
n = os.fork()
if n > 0:
    print("Parent PID: ",os.getpid())
	#While the child process is not completed
	#parent process will wait before exit
    
    while isDone.value is 0:
        pass
    
	#When the child process is completed, 
    #the parent process will also be completed.
    if isDone.value is 1:
        #print("Done")
        exit()

	#So, I prevented the Orphan process situaiton.
elif n == 0:
    print("Child PID: ",os.getpid())
    files = []
    thread_pool = [threading.Thread(target=downloadFile,args=(url,files,)) for url in urls]
    [thread.start() for thread in thread_pool]
    [thread.join() for thread in thread_pool]
    
    file_hashes = {}

    def hashFile(file):
        #time.sleep(1)
        file_content = open(file,"rb").read()
        file_hash = hashlib.md5(file_content).hexdigest()
        return file_hash

    def pushDictAndCheckDuplicates(file_hash):
        # Check if file_hash is in file_hashes
        if file_hash in file_hashes:
            # If exist, increment its value by 1
            print("Image is already exist.")
            file_hashes[file_hash] = file_hashes[file_hash] + 1
        else:
            # If not exist, set its value to 1
            print("Hash is: " + file_hash)
            file_hashes[file_hash] = 1

    # Hashing is a CPU bound process.
    # So we are going to split data into processes via Pool
    
    p = multiprocessing.Pool(processes=6)
    file_hashes_list = p.map(hashFile,files)

    # And check for duplicates
    for file_hash in file_hashes_list:
        pushDictAndCheckDuplicates(file_hash)
	
    """
    # This is for 1 process to measure performance
    for file in files:
    	file_hash = hashFile(file)
    	pushDictAndCheckDuplicates(file_hash)
    """
    ending_time = time.time()
    print("Passed time: " + str(ending_time - begin_time))
    isDone.value = 1
    exit()



