#!/usr/bin/env python3
###Zerwekh, Edwin
###SY402
import sys
import os
import hashlib 
import time ###Learned how to use this on tutorialspoint.com/python3/python_date_time.htm
import json ###Learned how to use this on https://www.geeksforgeeks.org/write-a-dictionary-to-a-file-in-python/


MasterDict={}
directoryDict={}
badDirs=['/dev','/proc','/run','/sys','/tmp','/var/lib','/var/run','/var/log','/snap','/usr/share']



def dirFinder(directory, dirList):
    for i in dirList:
        if i in directory:
            return(False)

def hashfunction(filename):
    try:
        fd=open(filename,'rb')        
        hashed=hashlib.sha256()
        hashed.update(fd.read())
        return(hashed.hexdigest())
    except:
        return(False)

    

def arrayComparison(goodArr, questionableArr, deltaArr, dirName):
    for i in goodArr:
        if i not in questionableArr:
            deltaArr.append(dirName+'/'+i)
            continue
    return()

def initScan():
    x=1
    for i in (os.walk('/', topdown=True)): ###Used https://docs.python.org/3/library/os.html to properly use the os.walk function

        if (dirFinder(i[0],badDirs)==False):
            continue

        #print(i[0])   ###Captures parent main directory
        directoryDict[i[0]]=i[2] ###These line create a dictionary where the key is the directory
            ###and the value is a list of all the files within it

        ###########################################################################################
        if x==1:                ###This if statement is here to correctly
            for j in i[2]:      ###Print the files of the first directory 
                #print(i[0]+j)
                try:
                    fd=open(i[0]+j,'rb')        ###Learned this hashing process from https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
                    hashed=hashlib.sha256()
                    hashed.update(fd.read())
                    currentTime = time.asctime(time.localtime(time.time()))
                    MasterDict[i[0]+j] = [j, i[0]+j, hashed.hexdigest(), currentTime]
                    fd.close()
                except:
                    print(i[0]+j)
                    continue
            x=0
            continue    ##Needed for first directory

        for j in i[2]:     ###Prints all files in the current directory being looked at
            #print(i[0]+'/'+j)

        ##################################################################################################
            try:
                fd=open(i[0]+'/'+j,'rb')        ###https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
                hashed=hashlib.sha256()
                hashed.update(fd.read())
                currentTime = time.asctime(time.localtime(time.time()))
                MasterDict[i[0]+'/'+j] = [j, i[0]+'/'+j, hashed.hexdigest(), currentTime]
                #print(MasterDict[i[0]+'/'+j])
                fd.close()
            except:
                print(i[0]+'/'+j)
    with open('masterDirectoryLog.txt','w') as masterDirectoryFile: ###Learned how to write a dictionary to a file on
        masterDirectoryFile.write(json.dumps(directoryDict)) ###https://www.geeksforgeeks.org/write-a-dictionary-to-a-file-in-python/
    with open('masterFileLog.txt','w') as masterFileLog:
        masterFileLog.write(json.dumps(MasterDict))
    return


def scan():
    refDirectoryDict=(json.load(open('masterDirectoryLog.txt','r'))) ###initialized dictionary of directorys as keys, values are list of files
    refFileDict=(json.load(open('masterFileLog.txt','r'))) ###initialized dictionary of absolute files as keys, valules are file info
    missingFiles=[]
    newFiles=[]
    changedFiles=[]
    
    for i in (os.walk('/', topdown=True)): ###Used https://docs.python.org/3/library/os.html to properly use the os.walk function

        if (dirFinder(i[0],badDirs)==False):
            continue
        arrayComparison(refDirectoryDict[i[0]], i[2], missingFiles, i[0])
        try:
            for j in i[2]:
                if j not in refDirectoryDict[i[0]]:
                    newFiles.append(i[0]+'/'+j)
                    continue
                elif hashfunction(i[0]+'/'+j) ==False:
                    continue
                elif hashfunction(i[0]+'/'+j) != refFileDict[(i[0]+'/'+j)][2]:
                    changedFiles.append(i[0]+'/'+j)
                    continue
                else:
                    continue
        except KeyError:
            continue
    for i in missingFiles:
        print('Missing files:'+i)
    for i in newFiles:
        print('New files:'+i)
    for i in changedFiles:
        print('Altered files:'+i)
            

        
    return



def main():
    if len(sys.argv)<2:
        print('-i for initial scan\n-s to scan machine and find new/altered files')
        return

    elif sys.argv[1]=='-i': ###First scan of machine
        initScan()
        return

    elif sys.argv[1]=='-s': ###Used to compare current state with referrenced state
        scan()
        return

    else:
        print('-i for initial scan\n-s to scan machine and find new/altered files')
        return

main()





# x=(json.load(open('masterDirectoryLog.txt','r')))
# print(x)
# print(x['./'])
