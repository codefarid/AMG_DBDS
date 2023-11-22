from DB import *
import os
import json
import pprint
import re

UPLOAD_FOLDER = './uploads' 

def getQuery():
    filename = 'test.sql'
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    f = open(file_path, "r")
    # sql_content = f.read()

    # # Memisahkan komentar dan query menggunakan ekspresi reguler
    # queries_and_comments = re.split(r'\s*;\n\s*', sql_content)

    # # Memisahkan komentar dari query
    # queries = [query.strip() for query in queries_and_comments if not query.startswith('--') and not query.startswith('/*')]

    # # Mendapatkan array komentar
    # comments = [comment.strip() for comment in queries_and_comments if comment.startswith('--') or comment.startswith('/*')]
    # print(queries)
    
    
    sqlFiles = f.read()
    f.close()
    
    otherCommands = sqlFiles.split('\n')
    sqlCommands = sqlFiles.split(';')
    tables = []
    
    for i in range(len(otherCommands)):
        lanes = otherCommands[i]
        comment = []
        queries = []
        if lanes.startswith('--') and lanes.endswith('--'):
            comentSplit = lanes.split('Query for')
            tableNames = []
            for x in range(len(comentSplit)):
                strings = comentSplit[x]
                concatStrings = ''
                for y in range(len(strings)):
                    if strings[y] != '-':
                        concatStrings += strings[y]
                
                tableNames.append(concatStrings)
            
            if tableNames[1] is not None:
                tables.append(tableNames[1])
        
    # for j in range(len(otherCommands)):
    #     lane = otherCommands[j]
    #     # print(lane.lower().startswith("create") or lane.lower().startswith("select") or lane.lower().startswith("alter") and lane.endswith(');') or lane.endswith(';'),lane ,j)
    #     if lane.lower().startswith("create") or lane.lower().startswith("select") or lane.lower().startswith("alter"):
    #         print(lane)
    isCol = []
    isCreateHeader = []
    isColSelect = []
    isAlter = []
    for j in sqlCommands:
        perlanes = j.split('\n')
        for k in perlanes:
            if not k.startswith('--') and not k.endswith('--'):
                if 'varchar' in k.lower() and not k.lower().startswith('add'):
                    isCol.append(k)
                    print(k)
                elif 'create table' in k.lower():
                    isCreateHeader.append(k)
                elif 'as' in k.lower():
                    isColSelect.append(k)
                elif "alter table" in k.lower() or "add" in k.lower():
                    isAlter.append(k)
                    print(k)
    
    
    return 'Wait'
    
        
    

print(getQuery())