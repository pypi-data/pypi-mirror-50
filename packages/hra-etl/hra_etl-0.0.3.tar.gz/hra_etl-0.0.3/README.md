# Python ETL Base Code

This project has the etl jupyter file for kick starting any new development, .whl file which has all the inbuilt etl functionality and boiler plate structure for any new integration.


*hra_etl library has following functions*

# BaseTable.decrypt (config file path,filename,path of the curretnt script,DSN name, flag)
  - flag = 0 (no addition of as of date and file would be in GF temp folder)
  - flag = 1 (as of date added and file will be in decypted folder)


```
from hra_etl import BaseTable
import os
import sys

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    filename = sys.argv[1]
    BaseTable.BaseTable.decrypt(path+"\\"+filename+".config",filename,path,'HRA','1')
```

# BaseTable.BaseTable.setup(path)
- where path is the location where the folders and files would be generated. Below are the folders and files it would generate on calling this function
  - Control file
    - It has 5 files WF(overall workflow control file), stg, base, base-audit, pkg.
  - Error_log
    - It would hold all teh error logs.
  - Unittest_log
    - to have all the logs for unittesting
  - bkp.txt
    - to store the bkp creation date.
```
from hra_etl import BaseTable
import os
import sys

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    BaseTable.BaseTable.setup(path)
```