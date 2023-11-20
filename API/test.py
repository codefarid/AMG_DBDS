from DB import *
import os
import json
import pprint
import re


cur_sql.execute("""
                SELECT 
                TBIDM1701 as 'id'
                FROM AAM1701
                WHERE TBIDM1701 LIKE 'PRMT%'
                """)
results = []
for row in cur_sql:
            results.append(dict(zip([column[0] for column in cur_sql.description], [str(x).strip() for x in row])))
