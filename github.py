import random   ##
import commands
import time
import multiprocessing
from multiprocessing import Process
import logging
import fileinput
#cmd = "git ls-remote github.com:Infoblox-CTO/xaas-web HEAD | tail -1"
#cmd = "git ls-remote github.com:Gopalkrish14/xaas-web HEAD | tail -1"

logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info('Main process start')

def trigger_driver(new_commit_id , git_name):

    ''' This function will execute the another script "CI_CD_Driver_XaaS_Functional" for running 
    the jenkins jobs.'''
    
    # Read in the file
    
    tempFile =  open('trigger_driver_monitor.log', 'r+')
        
    # Update the Log output file name

    for line in fileinput.input( 'trigger_driver_monitor.log' ):

        if "git_repo_1" in line :
            tempFile.write(line.replace("git_repo_1", git_name ))
        elif "git_repo_2" in line :
            tempFile.write(line.replace("git_repo_2", git_name ))
        elif "git_repo_3" in line :
            tempFile.write(line.replace("git_repo_3", git_name ))


    tempFile.close()

    filedata = None
    with open('file.txt', 'r') as file :
        file.seek(0)
        filedata = file.read()
    # Update the Log output file name
    filedata = filedata.replace('driver_monitor', new_commit_id)
    # Write the file out again
    with open('file.txt', 'w') as file:
        file.write(filedata)
    file.close()
    

    cmd1 = "cat trigger_driver_monitor.log"
    jobexec_cmd = commands.getoutput(cmd1)
    out1 = commands.getoutput(jobexec_cmd)

    #data = "./CI_CD_Driver_XaaS_Functional -f XaaS_Functional.yaml > logs/" + new_commit_id + ".log"
    #jobexec_cmd = commands.getoutput(data)
  
def clean_process_list(child_process):

    ''' This function will clean the no. of running process from the child_process list.
    First it will check the process is running or not and if process is completed their task
    then it will eleminate the entries from the child_process list. '''

    for index in range(len(child_process)):
        if(child_process[index].is_alive()):
            print "Thread " + child_process[index].name + " is still running"
            logging.info("Thread " + child_process[index].name + " is still running")
        else:
            if not (child_process[index] is None):
                print child_process[index]
                logging.info(child_process[index])
                child_process[index].terminate()
                print "Child " + child_process[index].name + " Completed successfully"
                logging.info("Child " + child_process[index].name + " Completed successfully")
                del child_process[index]
                break

def trigger_process(git_name):

    ''' Trigger_process function will trigger the process for running the jenkins job.
    For that first it will check that current running process which shouldn't be more then 5 and also 
    it will check the size of the commit_list for eleminating the error "Index Error: list index out of range".
    And if it is satisfy both the conditions then it will trigger the jenkins job and delete the commit_id 
    which is used for this process.
    '''

    global new_temp
    if len(child_process) < 5:
        if(commit_list <> []):
            if(new_temp != commit_list[1]):
                commit_id = commit_list[1]
                logging.info("commit id: %s  going for jenkin job: ", commit_id)
                print "commit id: %s  going for jenkin job: " % commit_id
                txt1 = open('commit_id.txt', 'w')
                txt1.seek(0)
                txt1.write(commit_id)
              
                temp1 = multiprocessing.Process(target = trigger_driver , args = (commit_id, git_name))
                temp1.start()
                txt1.close()

                ''' This Below if condition is using for eleminating the duplicate process running for last commit_id. '''

                if(len(commit_list) == 2):     
                    new_temp = commit_list[1]
                    print "new_temp value is: %s" % new_temp 
                else:
                    del commit_list[0]
                    del commit_list[0]
                child_process.append(temp1)
                time.sleep(45)

            else:
                del commit_list[0]
                    
no_of_current_running = 0
child_process = [] # list to store the process object

commit_list = ["git_repo_1","13"] #Default commit_id which will be on first postion.
new_temp = "90" 

while True:

    commit_id_from_repo_1 = random.randrange(11 , 19)
    commit_id_from_repo_2 = random.randrange(21 , 29)
    commit_id_from_repo_3 = random.randrange(31 , 39)
    commit_id_from_repo_1 = str(commit_id_from_repo_1)
    commit_id_from_repo_2 = str(commit_id_from_repo_2)
    commit_id_from_repo_3 = str(commit_id_from_repo_3)
    #out = commands.getoutput(cmd) #out is a variable which hold the latest commit_id from git-hub
    #out = out.split()[0]         
           
    if(commit_id_from_repo_1 == commit_list[len(commit_list) - 1]):  #comparing latest git-hub commit_id with recently added commit_id in commit_list.
        if(len(child_process) < 5):                #checking the current running process which should be less then 5.
            if(new_temp != commit_list[1]):        #eleminating the duplicate process running for last commit_id.
                trigger_process("git_repo_1")
                   
        print "No new commit sleep for 60 sec."
        logging.info("No new commit sleep for 60 sec.")
        time.sleep(60)
    else:
        commit_list.append("git_repo_1")
        commit_list.append(commit_id_from_repo_1)
        trigger_process("git_repo_1")
    

    if(commit_id_from_repo_2 == commit_list[len(commit_list) - 1]):  
        if(len(child_process) < 5):                
            if(new_temp != commit_list[1]):        
                trigger_process("git_repo_2")

        print "No new commit sleep for 60 sec."
        logging.info("No new commit sleep for 60 sec.")
        time.sleep(60)
    else:
        commit_list.append("git_repo_2")
        commit_list.append(commit_id_from_repo_2)
        trigger_process("git_repo_2")
    

    if(commit_id_from_repo_3 == commit_list[len(commit_list) - 1]):  
        if(len(child_process) < 5):                
            if(new_temp != commit_list[1]):        
                trigger_process("git_repo_3")

        print "No new commit sleep for 60 sec."
        logging.info("No new commit sleep for 60 sec.")
        time.sleep(60)
    else:
        commit_list.append("git_repo_3")
        commit_list.append(commit_id_from_repo_3)
        trigger_process("git_repo_3")

    logging.info("No. of commit_id in queue: " + str(commit_list))
    print "No. of commit_id in queue: " + str(commit_list)     
    clean_process_list(child_process)
    print "Number of current running child process : " + str(len(child_process))
    
    




