from DB import *
import os
import json
import pprint
import re

UPLOAD_FOLDER = './uploads' 

def getQuery():
    filename = 'AAM1101.sql'
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    f = open(file_path, "r")
    sqlFiles = f.read()
    f.close()
    sqlCommands = sqlFiles.split('\n')
    headerCreate = []
    closeCreate = []
    headerSelect = []
    closeSelect = []
    lanes = []
    cleaned = []
    getQuery = []
    for i in range(len(sqlCommands)):
        if 'CREATE TABLE'.lower() in sqlCommands[i].lower():
            headerCreate.append(i)
            lanes.append(i)
        if ')' == sqlCommands[i]:
            closeCreate.append(i)
            lanes.append(i)
            
            
        if 'SELECT'.lower() in sqlCommands[i].lower():
            headerSelect.append(i)
            lanes.append(i)
            
        if "FROM".lower() in sqlCommands[i].lower():
            closeSelect.append(i)
            lanes.append(i)
    index = 0
    
    while index < len(lanes):
        subarr = lanes[index:index + 2]
        cleaned.append(subarr)
        index += 2
        
    print(cleaned)

print(getQuery())