# import pyodbc
import pymssql

# try:
#     try:
#         DB = pyodbc.connect("DSN=order;User Id=BUMINA;Password=BUMINA;")
#     except:
#         DB = pyodbc.connect("DSN=ordertest;User Id=BUMINA;Password=BUMINA;")
# except:
#     print('Cant connect to DB2 Server')

test = True
# test = False

deploy_local = False
development = True

try:
    if test:
        DB_SQL = pymssql.connect('172.18.178.243', 'sa', '@sahi2420', "TestAMGAPPS")
        DB_SQL_AMG = pymssql.connect('172.18.178.243', 'sa', '@sahi2420', "TestAMG")
    else:
        DB_SQL = pymssql.connect('172.18.178.243', 'sa', '@sahi2420', "AMGAPPS")
        DB_SQL_AMG = pymssql.connect('172.18.178.243', 'sa', '@sahi2420', "AMG")
except:
    print('Cant connect to SQL Server')
    
cur_sql = DB_SQL.cursor()
cur_sql_amg = DB_SQL_AMG.cursor()