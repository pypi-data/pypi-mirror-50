import hra_etl.labio.configWrapper as ld_cg
from hra_etl.labio import logWrapper
import csv
import logging
import json
from datetime import datetime, timedelta
import os, time, sys
import codecs
import pyodbc
import threading
import pandas as pd
import subprocess
import shutil
import gnupg
import chardet

class BaseTable():
    __config = None
    __DSN = None
    __audit_values = []
    __idx = None
    __fpath = None

    def __init__(self, DSN):
        self.__DSN = DSN

    def load_configuration(self, file_name, path):
        try:
            self.__config = ld_cg.load_configuration(file_name)
            BaseTable.__config = self.__config
            self.__fpath = path
            BaseTable.__fpath = path
            self.__audit_values.append(datetime.now().strftime("%Y%m%d"))
            self.__audit_values.append(self.__config.stg_mapping)
            self.__audit_values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.__audit_values.append(self.__config.src_name)
            self.__audit_values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return True
        except:
            return False

    #Creating Table
    def create_tables(self):
        try:
            if self.create_stg_table():
                if self.create_base_audit_table():
                    if self.create_base_table():
                        if self.create_pkg_table():
                            self.control_file(0,'ct')
                            return True
        except:
            self.control_file(1,'ct')
            return False

    #connecting to Hadoop
    def hd_conn(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db = pyodbc.connect('DSN='+self.__DSN, autocommit=True)
            return db
        except Exception as e:
            self.error_log(1,st_date,e,'Hadoop connection')
            return False

    #Opening of File
    def open_file(self,file):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f = codecs.open(file, encoding = "utf-8-sig", errors ='replace')
            return f
        except Exception as e:
            self.error_log(0,st_date,e,'Read_csv_error')
            return False

    #Creating Stage Table
    def create_stg_table(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f = self.open_file(self.__config.input_file)
            if (f != False):
                csvreader = csv.reader(f, delimiter=self.__config.delimiter, quotechar='"',skipinitialspace=True)
                headers = next(csvreader)
                list_col=[]
                for col in list(headers):
                    if any(col in x  for x in self.__config.stg_timestamp)==True:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'timestamp'))
                    else:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'string'))
                for col in list(self.__config.stg_audit):
                    if any(col in x  for x in self.__config.stg_timestamp)==True:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'timestamp'))
                    else:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'string'))
                cmd = 'CREATE TABLE IF NOT EXISTS %s ( %s ) STORED AS PARQUET;' % (self.__config.stg_table, ','.join(list_col))
                db = self.hd_conn()
                if db !=False:
                    cur=db.cursor()
                    cur.execute(cmd)
                    db.commit()
                    f.close()
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            self.error_log(1,st_date,e,'stg_table_creation')
            return False

    #Create Base Audit Table
    def create_base_audit_table(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f = self.open_file(self.__config.input_file)
            if (f != False):
                csvreader = csv.reader(f, delimiter=self.__config.delimiter, quotechar='"',skipinitialspace=True)
                headers = next(csvreader)
                list_col=[]
                for col in list(headers):
                    if any(col in x  for x in self.__config.base_audit_timestamp)==True:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'timestamp'))
                    else:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'string'))
                for col in list(self.__config.base_audit_audit):
                    if any(col in x  for x in self.__config.base_audit_timestamp)==True:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'timestamp'))
                    else:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'string'))
                cmd = 'CREATE TABLE IF NOT EXISTS %s ( %s ) STORED AS PARQUET;' % (self.__config.base_audit_table, ','.join(list_col))
                db = self.hd_conn()
                if db !=False:
                    cur=db.cursor()
                    cur.execute(cmd)
                    db.commit()
                    f.close()
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            self.error_log(1,st_date,e,'base_audit_table_creation')
            return False

    #Create Base Table
    def create_base_table(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f = self.open_file(self.__config.input_file)
            if (f != False):
                csvreader = csv.reader(f, delimiter=self.__config.delimiter, quotechar='"',skipinitialspace=True)
                headers = next(csvreader)
                list_col=[]
                for col in list(headers):
                    if any(col in x  for x in self.__config.base_timestamp)==True:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'timestamp'))
                    else:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'string'))
                for col in list(self.__config.base_audit):
                    if any(col in x  for x in self.__config.base_timestamp)==True:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'timestamp'))
                    else:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'string'))
                cmd = 'CREATE TABLE IF NOT EXISTS %s ( %s ) STORED AS PARQUET;' % (self.__config.base_table, ','.join(list_col))
                db = self.hd_conn()
                if db !=False:
                    cur=db.cursor()
                    cur.execute(cmd)
                    db.commit()
                    f.close()
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            self.error_log(1,st_date,e,'base_table_creation')
            return False

    #Create Pkg Table
    def create_pkg_table(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f = self.open_file(self.__config.input_file)
            if (f != False):
                csvreader = csv.reader(f, delimiter=self.__config.delimiter, quotechar='"',skipinitialspace=True)
                headers = next(csvreader)
                list_col=[]
                for col in list(headers):
                    if any(col in x  for x in self.__config.pkg_timestamp)==True:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'timestamp'))
                    else:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'string'))
                for col in list(self.__config.pkg_audit):
                    if any(col in x  for x in self.__config.pkg_timestamp)==True:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'timestamp'))
                    else:
                        list_col.append("{0} {1}".format(str(col).replace(" ", "_").replace('/', '_').replace('#', '_').replace('-','_').replace('(','').replace(')',''), 'string'))
                cmd = 'CREATE TABLE IF NOT EXISTS %s ( %s ) STORED AS PARQUET;' % (self.__config.pkg_table, ','.join(list_col))
                db = self.hd_conn()
                if db !=False:
                    cur=db.cursor()
                    cur.execute(cmd)
                    db.commit()
                    f.close()
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            self.error_log(1,st_date,e,'pkg_table_creation')
            return False

    #Loading into STG table
    def load_into_stg(self):
        try:
            idx = 0
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db = self.hd_conn()
            if db !=False:
                cur=db.cursor()
                full_cmd = 'TRUNCATE TABLE %s' % (self.__config.stg_table)
                cur.execute(full_cmd)
                self.split_files()
                arr = []
                i=-1
                filelist = [ f for f in os.listdir(self.__fpath+'\\temp') if f.endswith('.'+str(self.__config.format)) ]       
                for f in filelist:
                    i=i+1
                    arr.append(threading.Thread(target=self.file_to_lake, args=(self.__fpath+'\\temp'+'\\'+f,)))
                    arr[i].start()
                for j in arr:
                    j.join()
                filelist = [ f for f in os.listdir(self.__fpath+'\\temp') if f.endswith('.'+str(self.__config.format))]
                for f in filelist:
                    os.remove(self.__fpath+'\\temp'+'\\'+f)
                if os.path.exists(self.__fpath+'\\temp'):
                    os.rmdir(self.__fpath+'\\temp')
                self.error_log(0,st_date,"Mapping successfull",self.__config.stg_mapping)
                self.control_file(0,'stg')
                return True
        except Exception as e:
            self.error_log(1,st_date,e,self.__config.stg_mapping)
            self.control_file(1,'stg')
            return False


    #Splitting the files into small files

    def split_files(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f = self.open_file(self.__config.input_file)
            if (f != False):
                csvfile = f.readlines()
                num = 1
                print(len(csvfile))
                di = int(len(csvfile)/self.__config.thread)
                if di > 1100:
                    self.__idx = 1000
                else:
                    self.__idx = int(di*0.8)
                
                if not os.path.exists(self.__fpath+'\\temp'):
                    os.makedirs(self.__fpath+'\\temp')
                if len(csvfile)<=3000:
                    codecs.open(self.__fpath+'\\temp'+'\\'+'Proc_' + str(num) + '.'+str(self.__config.format), 'w+', encoding = "utf8", errors ='replace').writelines(csvfile[1:len(csvfile)])
                    self.__idx = 1000
                else:
                    for i in range(len(csvfile)):
                        if i % di == 0:
                            if i!=0:
                                codecs.open(self.__fpath+'\\temp'+'\\'+'Proc_' + str(num) + '.'+str(self.__config.format), 'w+', encoding = "utf8", errors ='replace').writelines(csvfile[i:i+int(len(csvfile)/self.__config.thread)])
                                num += 1
                            else:
                                codecs.open(self.__fpath+'\\temp'+'\\'+'Proc_' + str(num) + '.'+str(self.__config.format), 'w+', encoding = "utf8", errors ='replace').writelines(csvfile[1:i+int(len(csvfile)/self.__config.thread)])
                                num += 1
                return True
        except Exception as e:
            self.error_log(1,st_date,e,'Split_File')
            return False

    #Loading from file to table
    def file_to_lake(self,file_name):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db = self.hd_conn()
            if db !=False:
                cur=db.cursor()
                f = self.open_file(file_name)
                if f != False:
                    csvreader = csv.reader(f, delimiter=self.__config.delimiter)
                    list_cmd=[]
                    i = 0
                    for row in csvreader:
                        fields=[]
                        for j in range(len(row)):
                            fields.append('"'+str(row[j]).replace("'","\\'")+'"')
                        for k in range(len(self.__audit_values)):
                            fields.append('"'+str(self.__audit_values[k])+'"')
                        cmd = "(" + ','.join(fields) + ")"
                        i += 1
                        list_cmd.append(str(cmd))
                        if i == self.__idx:
                            full_cmd = 'INSERT INTO TABLE {0} VALUES {1};'.format(self.__config.stg_table, ', '.join(list_cmd))
                            cur.execute(full_cmd)    
                            i = 0
                            list_cmd = []
                    if len(list_cmd) > 0:
                        full_cmd = 'INSERT INTO TABLE {0} VALUES {1};'.format(self.__config.stg_table, ', '.join(list_cmd))
                        cur.execute(full_cmd)
                    f.close()
        except Exception as e:
            self.error_log(1,st_date,e,self.__config.stg_mapping)

    #Loading From one table to other table in hadoop
    def load_into_base_audit(self):
        st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            db = self.hd_conn()
            if db !=False:
                cur=db.cursor()
                full_cmd = 'Drop table IF EXISTS %s purge' % (self.__config.base_audit_table+'_temp')
                cur.execute(full_cmd)
                cur=db.cursor()
                full_cmd = 'SELECT * FROM %s' % (self.__config.stg_table)
                cur.execute(full_cmd)
                data = cur.fetchall()
                cur=db.cursor()
                ct_temp = 'CREATE TABLE IF NOT EXISTS %s as select * from %s;' % (self.__config.base_audit_table+'_temp',self.__config.base_audit_table)
                cur.execute(ct_temp)
                arr = []
                di = int(len(data)/self.__config.thread)
                if di > 1100:
                    self.__idx = 1000
                    for i in range(self.__config.thread):
                        dt = data[round(len(data)*(i/self.__config.thread)):round(len(data)*((i+1)/self.__config.thread))]
                        arr.append(threading.Thread(target=self.insert_data, args=(dt,self.__config.stg_mapping,self.__config.base_audit_mapping,self.__config.base_audit_table+'_temp')))
                        arr[i].start()
                else:
                    self.__idx = int(di*0.8)
                    arr.append(threading.Thread(target=self.insert_data, args=(data,self.__config.stg_mapping,self.__config.base_audit_mapping,self.__config.base_audit_table+'_temp')))
                    arr[0].start()
                for j in arr:
                    j.join()
                cur=db.cursor()
                cur.execute("compute stats "+self.__config.base_audit_table+'_temp')
                cur.execute("refresh "+self.__config.base_audit_table+'_temp')

            self.error_log(0,st_date,"Mapping successfull",self.__config.base_audit_mapping)
            self.control_file(0,'base_audit')
            return True
        except Exception as e:
            self.error_log(1,st_date,e,self.__config.base_audit_mapping)
            self.control_file(1,'base_audit')
            return False
    
    #Loading into Base from Base Audit
    def load_into_base(self):
        st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            db = self.hd_conn()
            if db !=False:
                cur=db.cursor()
                full_cmd = 'Drop table IF EXISTS %s purge' % (self.__config.base_audit_table+'_temp')
                cur.execute(full_cmd)
                cur=db.cursor()
                full_cmd = 'SELECT * FROM %s' % (self.__config.stg_table)
                cur.execute(full_cmd)
                data = cur.fetchall()
                cur=db.cursor()
                ct_temp = 'CREATE TABLE IF NOT EXISTS %s as select * from %s;' % (self.__config.base_table+'_temp',self.__config.base_table)
                cur.execute(ct_temp)
                arr = []
                di = int(len(data)/self.__config.thread)
                if di > 1100:
                    self.__idx = 1000
                    for i in range(self.__config.thread):
                        dt = data[round(len(data)*(i/self.__config.thread)):round(len(data)*((i+1)/self.__config.thread))]
                        arr.append(threading.Thread(target=self.insert_data, args=(dt,self.__config.stg_mapping,self.__config.base_mapping,self.__config.base_table+'_temp')))
                        arr[i].start()
                else:
                    self.__idx = int(di*0.8)
                    arr.append(threading.Thread(target=self.insert_data, args=(data,self.__config.stg_mapping,self.__config.base_mapping,self.__config.base_table+'_temp')))
                    arr[0].start()
                for j in arr:
                    j.join()
                cur=db.cursor()
                cur.execute("compute stats "+self.__config.base_table+'_temp')
                cur.execute("refresh "+self.__config.base_table+'_temp')

            self.error_log(0,st_date,"Mapping successfull",self.__config.base_mapping)
            self.control_file(0,'base')
            return True
        except Exception as e:
            self.error_log(1,st_date,e,self.__config.base_mapping)
            self.control_file(1,'base')
            return False

    #Loading into Base from Base Audit
    def load_into_pkg(self):
        st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            db = self.hd_conn()
            if db !=False:
                cur=db.cursor()
                full_cmd = 'Drop table IF EXISTS %s purge' % (self.__config.pkg_table+'_temp')
                cur.execute(full_cmd)
                cur=db.cursor()
                full_cmd = 'SELECT * FROM %s' % (self.__config.stg_table)
                cur.execute(full_cmd)
                data = cur.fetchall()
                cur=db.cursor()
                ct_temp = 'CREATE TABLE IF NOT EXISTS %s as select * from %s;' % (self.__config.pkg_table+'_temp',self.__config.pkg_table)
                cur.execute(ct_temp)
                arr = []
                di = int(len(data)/self.__config.thread)
                if di > 1100:
                    self.__idx = 1000
                    for i in range(self.__config.thread):
                        dt = data[round(len(data)*(i/self.__config.thread)):round(len(data)*((i+1)/self.__config.thread))]
                        arr.append(threading.Thread(target=self.insert_data, args=(dt,self.__config.stg_mapping,self.__config.pkg_mapping,self.__config.pkg_table+'_temp')))
                        arr[i].start()
                else:
                    self.__idx = int(di*0.8)
                    arr.append(threading.Thread(target=self.insert_data, args=(data,self.__config.stg_mapping,self.__config.pkg_mapping,self.__config.pkg_table+'_temp')))
                    arr[0].start()
                for j in arr:
                    j.join()
                cur=db.cursor()
                cur.execute("compute stats "+self.__config.pkg_table+'_temp')
                cur.execute("refresh "+self.__config.pkg_table+'_temp')

            self.error_log(0,st_date,"Mapping successfull",self.__config.pkg_mapping)
            self.control_file(0,'pkg')
            return True
        except Exception as e:
            self.error_log(1,st_date,e,self.__config.pkg_mapping)
            self.control_file(1,'pkg')
            return False

    #Load into Layer to Layer
    def layer_to_layer(self,layer1,layer2,table1,table2,mapping1,mapping2):
        st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            db = self.hd_conn()
            if db !=False:
                cur=db.cursor()
                full_cmd = 'Drop table IF EXISTS %s purge' % (table2+'_temp')
                cur.execute(full_cmd)
                cur=db.cursor()
                full_cmd = 'SELECT * FROM %s' % (table1)
                cur.execute(full_cmd)
                data = cur.fetchall()
                cur=db.cursor()
                ct_temp = 'CREATE TABLE IF NOT EXISTS %s as select * from %s;' % (table2+'_temp',table2)
                cur.execute(ct_temp)
                cur=db.cursor()
                ct_temp = 'Truncate table IF EXISTS %s ' % (table2+'_temp')
                cur.execute(ct_temp)
                arr = []
                di = int(len(data)/self.__config.thread)
                if di > 1100:
                    self.__idx = 1000
                    for i in range(self.__config.thread):
                        dt = data[round(len(data)*(i/self.__config.thread)):round(len(data)*((i+1)/self.__config.thread))]
                        arr.append(threading.Thread(target=self.insert_data, args=(dt,mapping1,mapping2,table2+'_temp')))
                        arr[i].start()
                else:
                    self.__idx = int(di*0.8)
                    arr.append(threading.Thread(target=self.insert_data, args=(data,mapping1,mapping2,table2+'_temp')))
                    arr[0].start()
                for j in arr:
                    j.join()
                cur=db.cursor()
                cur.execute("compute stats "+table2+'_temp')
                cur.execute("refresh "+table2+'_temp')

            self.error_log(0,st_date,"Mapping successfull",mapping2)
            self.control_file(0,layer2)
            return True
        except Exception as e:
            self.error_log(1,st_date,e,mapping2)
            self.control_file(1,layer2)
            return False

    #Inserting Data into Hadoop
    def insert_data(self,data,mapping_name1,mapping_name2,target_table_name):
        list_cmd=[]
        idx1 = 0
        db = self.hd_conn()
        if db !=False:
            for row in data:
                fields=[]
                for j in range(len(row)):
                    if "'" in str(row[j]):
                        fields.append('"'+str(row[j]).replace(mapping_name1,mapping_name2).replace("'","\\'")+'"')
                    else:
                        fields.append("'"+str(row[j]).replace(mapping_name1, mapping_name2).replace("'","\\'")+"'")
                cmd = "(" + ','.join(fields) + ")"
                idx1 += 1
                list_cmd.append(str(cmd))
                if idx1 == self.__idx:
                    cur=db.cursor()
                    full_cmd = 'INSERT INTO TABLE %s VALUES %s;' % (target_table_name, ', '.join(list_cmd))
                    cur.execute(full_cmd)
                    idx1 = 0
                    list_cmd = []
            if len(list_cmd) > 0:
                cur=db.cursor()
                full_cmd = 'INSERT INTO TABLE %s VALUES %s;' % (target_table_name, ', '.join(list_cmd))
                cur.execute(full_cmd)

    #PreTest Checks
    def pretest_check(self):
        try:
            if self.stg_fields_cnt_chk():
                if self.file_dup_chk():
                    return True
                else:
                    self.control_file(1,'stg')
                    return False
            else:
                self.control_file(1,'stg')
                return False
        except Exception as e:
            self.control_file(1,'stg')
            return False

    #STG Test CHeck
    def stg_test(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f = self.open_file(self.__config.input_file)
            if (f != False):
                csvreader = csv.reader(f, delimiter=self.__config.delimiter)
                next(csvreader)
                file_cnt = len(list(csvreader))
                db = self.hd_conn()
                if db !=False:
                    full_cmd = 'SELECT count(*) FROM {0}'.format(self.__config.stg_table)
                    cur = db.cursor()
                    cur.execute(full_cmd)
                    stg = cur.fetchone()
                    if file_cnt == stg[0]:
                        self.unittest_log("Stg Count Check is Successfull "+ str(stg[0]),"stg_count_test")
                        f.close()
                        return True
                    else:
                        self.control_file(1,'stg')
                        self.unittest_log("Stg Count Check Failed with stg count as "+ str(stg[0]) + " and file count as "+str(file_cnt),"stg_count_test")
                        f.close()
                        return False
        except Exception as e:
            f.close()
            self.control_file(1,'stg')
            self.error_log(1,st_date,e,"stg_count_test")
            return False


    #Base Audit Test CHeck

    def base_audit_test(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db = self.hd_conn()
            if db !=False:
                full_cmd = 'SELECT as_of_date FROM {0}'.format(self.__config.stg_table)
                cur = db.cursor()
                cur.execute(full_cmd)
                tt=cur.fetchall()
                if len(tt)>0:
                    full_cmd = 'SELECT count(*) FROM {0}'.format(self.__config.stg_table)
                    cur = db.cursor()
                    cur.execute(full_cmd)
                    stg = cur.fetchone()
                    full_cmd = 'SELECT count(*) FROM {0} where as_of_date = "{1}"'.format(self.__config.base_audit_table+'_temp', str(tt[0][0]))
                    cur = db.cursor()
                    cur.execute(full_cmd)
                    base = cur.fetchone()
                    if base[0] == stg[0]:
                        cur = db.cursor()
                        with open(self.__fpath+'\\bkp.txt', "r") as f:
                            value = f.readline()
                        cmd = 'ALTER TABLE %s RENAME TO %s' %(self.__config.base_audit_table,self.__config.base_audit_table+'_bkp_'+str(value))
                        cur.execute(cmd)
                        cmd = 'ALTER TABLE %s RENAME TO %s' %(self.__config.base_audit_table+'_temp',self.__config.base_audit_table)
                        cur.execute(cmd)
                        self.unittest_log("Base Audit Count Check is Successfull "+ str(base[0]),"base_audit_count_test")
                        return True
                    else:
                        self.control_file(1,'base_audit')
                        self.unittest_log("Base Audit Check Failed with base audit count as "+ str(base[0]) + " and stg count as "+str(stg[0]),"base_audit_count_test")
                        return False
                else:
                    self.unittest_log("Base Audit Count Check is Successfull ","base_audit_count_test")
                    return True
            else:
                self.control_file(1,'base_audit')
                return False
        except Exception as e:
            self.control_file(1,'base_audit')
            self.error_log(1,st_date,e,"base_audit_count_test")
            return False
    #Base Test CHeck
    def base_test(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db = self.hd_conn()
            if db !=False:
                full_cmd = 'SELECT as_of_date FROM {0}'.format(self.__config.stg_table)
                cur = db.cursor()
                cur.execute(full_cmd)
                tt=cur.fetchall()
                if len(tt)>0:
                    full_cmd = 'SELECT count(*) FROM {0}'.format(self.__config.stg_table)
                    cur = db.cursor()
                    cur.execute(full_cmd)
                    stg = cur.fetchone()
                    full_cmd = 'SELECT count(*) FROM {0} where as_of_date = "{1}"'.format(self.__config.base_table+'_temp', str(tt[0][0]))
                    cur = db.cursor()
                    cur.execute(full_cmd)
                    base = cur.fetchone()
                    if base[0] == stg[0]:
                        cur = db.cursor()
                        with open(self.__fpath+'\\bkp.txt', "r") as f:
                            value = f.readline()
                        cmd = 'ALTER TABLE %s RENAME TO %s' %(self.__config.base_table,self.__config.base_table+'_bkp_'+str(value))
                        cur.execute(cmd)
                        cmd = 'ALTER TABLE %s RENAME TO %s' %(self.__config.base_table+'_temp',self.__config.base_table)
                        cur.execute(cmd)
                        self.unittest_log("Base Count Check is Successfull "+ str(base[0]),"base_count_test")
                        return True
                    else:
                        self.control_file(1,'base')
                        self.unittest_log("Base Check Failed with base count as "+ str(base[0]) + " and stg count as "+str(stg[0]),"base_count_test")
                        return False
                else:
                    self.unittest_log("Base Count Check is Successfull ","base_count_test")
                    return True
            else:
                self.control_file(1,'base')
                return False
        except Exception as e:
            self.control_file(1,'base')
            self.error_log(1,st_date,e,"base_count_test")
            return False

    #Pkg Test CHeck
    def pkg_test(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db = self.hd_conn()
            if db !=False:
                full_cmd = 'SELECT as_of_date FROM {0}'.format(self.__config.stg_table)
                cur = db.cursor()
                cur.execute(full_cmd)
                tt=cur.fetchall()
                if len(tt)>0:
                    full_cmd = 'SELECT count(*) FROM {0}'.format(self.__config.stg_table)
                    cur = db.cursor()
                    cur.execute(full_cmd)
                    stg = cur.fetchone()
                    full_cmd = 'SELECT count(*) FROM {0} where as_of_date = "{1}"'.format(self.__config.pkg_table+'_temp', str(tt[0][0]))
                    cur = db.cursor()
                    cur.execute(full_cmd)
                    pkg = cur.fetchone()
                    if pkg[0] == stg[0]:
                        cur = db.cursor()
                        with open(self.__fpath+'\\bkp.txt', "r") as f:
                            value = f.readline()
                        cmd = 'ALTER TABLE %s RENAME TO %s' %(self.__config.pkg_table,self.__config.pkg_table+'_bkp_'+str(value))
                        cur.execute(cmd)
                        cmd = 'ALTER TABLE %s RENAME TO %s' %(self.__config.pkg_table+'_temp',self.__config.pkg_table)
                        cur.execute(cmd)
                        self.unittest_log("Pkg Count Check is Successfull "+ str(pkg[0]),"pkg_count_test")
                        return True
                    else:
                        self.control_file(1,'pkg')
                        self.unittest_log("Pkg Check Failed with pkg count as "+ str(pkg[0]) + " and stg count as "+str(stg[0]),"pkg_count_test")
                        return False
                else:
                    self.unittest_log("Pkg Count Check is Successfull ","pkg_count_test")
                    return True
            else:
                self.control_file(1,'pkg')
                return False
        except Exception as e:
            self.control_file(1,'pkg')
            self.error_log(1,st_date,e,"pkg_count_test")
            return False

    def stg_fields_cnt_chk(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f = self.open_file(self.__config.input_file)
            if (f != False):
                csvreader = csv.reader(f, delimiter=self.__config.delimiter)
                headers = next(csvreader)
                db = self.hd_conn()
                if db !=False:
                    cur = db.cursor()
                    full_cmd = 'describe {0}'.format(self.__config.stg_table)
                    cur.execute(full_cmd)
                    data = cur.fetchall()
                    if len(headers)+ len(self.__config.stg_audit) == len(data):
                        self.unittest_log("Src file & Stg table headers count check Successfull","field_cnt_check")
                        f.close()
                        return True
                    else:
                        self.unittest_log("Src file & Stg table headers count check Failed","field_cnt_check")
                        f.close()
                        return False
        except Exception as e:
            f.close()
            self.error_log(1,st_date,e,'field_cnt_check')
            return False

    def file_dup_chk(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df = pd.read_csv(self.__config.input_file, sep=self.__config.delimiter)
            mylist = self.__config.flt
            if mylist:
                if(any(df[mylist].duplicated())):
                    self.unittest_log("Duplicate found in file","Duplicate_Check")
                    return False
                else:
                    self.unittest_log("No Duplicate found in file","Duplicate_Check")
                    return True
            else:
                return True
        except Exception as e:
            self.error_log(1,st_date,e,'Duplicate_Check')
            return False

    #Error Log Writer writes it to Error log folder
    def error_log(self,flg,st_date, log_message,file_name):
        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        path = self.__fpath+"\\Error_Log\\%s" %(file_name)
        timer = datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
        fileh = logging.FileHandler(path+timer+".log", 'a')
        formatter = logging.Formatter("LOG TYPE  -  %(levelname)s log \n\nSTART_DATE - {0} \n\nEND_DATE  -  {1}\n\nMAPPING   - {2}\n\nMESSAGE - \n%(message)s".format(st_date, t ,file_name))
        fileh.setFormatter(formatter)
        log = logging.getLogger()  # root logger
        for hdlr in log.handlers[:]:  # remove all old handlers
                log.removeHandler(hdlr)
        log.addHandler(fileh)
        log.setLevel(logging.DEBUG)
        if flg==0:
                logging.info(log_message)
                
        else:
                logging.error(log_message)

    #Writing Logging File
    def control_file(self,value,mapping):
        path = self.__fpath+'\\Control_File\\%s.log' %(mapping)
        file = open(path, "w")
        file.write(str(value))
        file.close()

    def unittest_log(self,log_message,file_name):
	    timer = datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
	    path = self.__fpath+'\\Unittest_Log\\%s' %(file_name)
	    file = open(path+timer+".log", "a")
	    file.write(str(log_message))
	    file.write('\n')
	    file.close()

    def read_control(self,name):
        try:
            path = self.__fpath+"\\Control_File\\%s.log" %(name)
            with open(path, "r") as f:
                value = f.readline()
            return int(value)
        except Exception as e:
            return False

    def purge_log(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            how_many_days_old_logs_to_remove = self.__config.number
            now = time.time()
            only_files = [self.__fpath+'\\Error_Log',self.__fpath+'\\Unittest_Log']
            for i in only_files:
                for file in os.listdir(i):
                    file_full_path = os.path.join(i,file)
                    if os.path.isfile(file_full_path) and file.endswith('.log'):
                        #Delete files older than x days
                        if os.stat(file_full_path).st_mtime < now - how_many_days_old_logs_to_remove * 86400: 
                            os.remove(file_full_path)
            return True
        except Exception as e:
            self.error_log(1,st_date,e,'Log Purging')
            return False

    def purge_table(self):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            today = now.strftime("%d%m%y")
            current_date = now
            now = datetime.now() - timedelta(days=self.__config.start_day)
            start_date = now
            now = datetime.now() - timedelta(days=self.__config.end_day)
            end_date = now
            start_time = time.time()
            db = self.hd_conn()
            if db !=False:
                cur = db.cursor()
                for i in pd.date_range(end_date,start_date):
                    if current_date > i:
                        cur.execute("Drop table IF EXISTS %s purge" % (self.__config.base_audit_table+"_bkp_"+i.strftime("%d%m%y")))
                        cur.execute("Drop table IF EXISTS %s purge" % (self.__config.base_table+"_bkp_"+i.strftime("%d%m%y")))
                        cur.execute("Drop table IF EXISTS %s purge" % (self.__config.pkg_table+"_bkp_"+i.strftime("%d%m%y")))
                        return True
                    else:
                        return True
        except Exception as e:
            self.error_log(1,st_date,e,'Table Purging')
            return False

    def purge_pgp(self,name):
        try:
            st_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_ends_with = ".pgp"
            how_many_days_old_logs_to_remove = self.__config.number
            now = time.time()
            archive_folder = os.path.join(self.__config.archive_folder, 'Archive')
            for filename in os.listdir(archive_folder):
                file_full_path = os.path.join(archive_folder,filename)
                if os.path.isfile(file_full_path) and filename.endswith(file_ends_with) and filename.startswith(name):
                    #Delete files older than x days
                    if os.stat(file_full_path).st_mtime < now - how_many_days_old_logs_to_remove * 86400: 
                        os.remove(file_full_path)
            return True
        except Exception as e:
            self.error_log(1,st_date,e,'Pgp Purging')
            return False

    def setup(path):
        try:
            if not os.path.exists(path+'\Control_file'):
                os.makedirs(path+'\Control_file')
            if not os.path.exists(path+'\Error_Log'):
                os.makedirs(path+'\Error_Log')
            if not os.path.exists(path+'\\Unittest_Log'):
                os.makedirs(path+'\\Unittest_Log')
            if not os.path.exists(path+'\\bkp.txt'):
                now = datetime.now()
                f= open(path+'\\bkp.txt',"w+")
                today = now.strftime("%d%m%y")
                f.write(today)
                f.close()
        except Exception as e:
            print(e)

    def flow(filename,my_instance,path,table_name):
        try:
            cfg_loaded = my_instance.load_configuration(filename,path)
            wf = my_instance.read_control('wf')
            if cfg_loaded:
                my_instance.control_file(1,'wf')
                if my_instance.read_control('ct') == wf:
                    tables_created = my_instance.create_tables()
                    if tables_created:
                        pretest = my_instance.pretest_check()
                        if pretest !=True:
                            my_instance.control_file(1,'ct')
                            my_instance.control_file(1,'stg')
                            my_instance.control_file(1,'base_audit')
                            my_instance.control_file(1,'base')
                            my_instance.control_file(1,'pkg')
                            raise Exception ('PreTest Error')
                    else:
                        my_instance.control_file(1,'ct')
                        my_instance.control_file(1,'stg')
                        my_instance.control_file(1,'base_audit')
                        my_instance.control_file(1,'base')
                        my_instance.control_file(1,'pkg')
                        raise Exception ('Table Creation Error')

                if my_instance.read_control('stg') == wf:
                    stg_loaded = my_instance.load_into_stg()
                    if stg_loaded:
                        stg_test = my_instance.stg_test()
                        if stg_test != True:
                            my_instance.control_file(1,'base_audit')
                            my_instance.control_file(1,'base')
                            my_instance.control_file(1,'pkg')
                            raise Exception ('Stg Test Error')
                    else:
                        my_instance.control_file(1,'base_audit')
                        my_instance.control_file(1,'base')
                        my_instance.control_file(1,'pkg')
                        raise Exception ('Stg Load Error')

                if my_instance.read_control('base_audit') == wf:
                    base_audit_loaded = my_instance.load_into_base_audit()
                    if base_audit_loaded:
                        base_audit_test = my_instance.base_audit_test()
                        if base_audit_test != True:
                            my_instance.control_file(1,'base')
                            my_instance.control_file(1,'pkg')
                            raise Exception ('Base Audit Test Error')
                    else:
                        my_instance.control_file(1,'base')
                        my_instance.control_file(1,'pkg')
                        raise Exception ('Base Audit Load Error')

                if my_instance.read_control('base') == wf:
                    base_loaded = my_instance.load_into_base()
                    if base_loaded:
                        base_test = my_instance.base_test()
                        if base_test != True:
                            my_instance.control_file(1,'pkg')
                            raise Exception ('Base Test Error')
                    else:
                        my_instance.control_file(1,'pkg')
                        raise Exception ('Base Load Error')

                if my_instance.read_control('pkg') == wf:
                    pkg_loaded = my_instance.load_into_pkg()
                    if pkg_loaded:
                        pkg_test = my_instance.pkg_test()
                        if pkg_test != True:
                            raise Exception ('Pkg Test Error')
                    else:
                        raise Exception ('Pkg Load Error')

                if my_instance.purge_log()!=True:
                    raise Exception ('Purge Log Error')

                if my_instance.purge_table()!=True:
                    raise Exception ('Purge Table Error')

                if my_instance.purge_pgp(table_name)!=True:
                    raise Exception ('Purge pgp Error')
                
                now = datetime.now()
                today = now.strftime("%d%m%y")
                file1 = open(path+'\\bkp.txt', "w")
                file1.write(today)
                file1.close()

                my_instance.control_file(0,'wf')
        except Exception as e:
            print(e)

    def transfer_file(self,pgp_file,logging):
        try:
            archive_folder = os.path.join(self.__config.archive_folder, 'Archive')
            if not os.path.exists(archive_folder):  # look if archive folder exist
                logging.warning("path doesn't exist: " + archive_folder)
                os.mkdir(archive_folder)  # make archive folder
                os.chmod(archive_folder, 0o777)  # give full permission to archive folder

            new_place = os.path.join(archive_folder, pgp_file)
            if os.path.isfile(new_place):
                os.remove(new_place)
            shutil.move(os.path.join(self.__config.input_folder, pgp_file),
                        new_place)  # move pgp file to new_place

            """output_path = os.path.join(file_config.output_folder,
                                       newname_decrypted_file)
            input_path = os.path.join(file_config.input_folder, decrypted_file)
            shutil.move(input_path, output_path)"""  # move decrypted file to output_path

            logging.info('[-] file moved: ' + pgp_file)
            return pgp_file
        except Exception as e:
            print('error')
            logging.error(e)

    def include_date(self,path, file, logging):
        try:
            path_and_name = os.path.join(path, file)
            numbers = path_and_name.rfind('_')
            numbers1 = file.rfind('_')
            new_name = '%s%s.%s' % (self.__config.archive_folder,file[:numbers1],self.__config.format)
            rawdata = open(path_and_name, 'rb').read()
            result = chardet.detect(rawdata)

            with codecs.open(path_and_name, 'r',encoding = result['encoding']) as old_file:
                date = path_and_name[numbers + 1:path_and_name.find('.',
                        numbers)]
                date = '"%s-%s-%s:00:00:00"' % (date[:4], date[4:6], date[6:])  # formatting
                with codecs.open(new_name, 'w', encoding = "utf8") as new_file:
                    old_line = old_file.readline()
                    old_line = old_line.replace('\n', '').replace('\r', '')
                    if old_line.endswith(self.__config.delimiter):
                        old_line = old_line[:-1]
                    new_file.write('%s%s"As of date"\n' % (old_line,self.__config.delimiter))
                    for line in old_file:
                        if len(line) < 1:
                            break
                        line = line.replace('\n', '').replace('\r', '')
                        if line.endswith(self.__config.delimiter):
                            line = line[:-1]
                        new_file.write('%s%s%s\n' % (line,self.__config.delimiter,date))
            os.remove(path_and_name)
        except Exception as e:
            print('error')
            logging.error(e)

    def searchFile(self,
        file_needed,
        local,
        end_time,logging):
        try:
            while time.time() < end_time:
                same_name_files = []
                for f in os.listdir(local):  # get all files on local
                    if f.endswith('pgp') and f.startswith(file_needed):
                        same_name_files.append(f)
                if same_name_files:
                    if len(same_name_files) == 1:
                        return same_name_files[0]
                    current_old_file_name = ''
                    current_old_file_number = float('inf')  # to get the first item of the same_name_files

                    for f in same_name_files:
                        digits = int(f[f.rfind('_') + 1:f.find('.')])
                        if digits < current_old_file_number:
                            current_old_file_number = digits
                            current_old_file_name = f
                    if not current_old_file_name:
                        logging.error('Sorry, Something is wrong with file date, please check filename.')
                        sys.stdout.write('ERROR')
                        sys.exit(1)
                    return current_old_file_name
                time.sleep(1)
            logging.error("Sorry after executing for 20 min, can't found the file")
            sys.stdout.write("Sorry after executing for 20 min, can't found the file")
            sys.exit(1)
        except Exception as e:
            print(e)
            logging.error(e)

    def pgp_decrypt(self,pgpexe,input_folder,output_folder,filename,passphrase):
        try:
            gpg = gnupg.GPG(gpgbinary=pgpexe)
            pgpfull_name = (os.path.join(input_folder, filename)).encode('utf-8')
            pfull_name = os.path.join(output_folder, filename.replace('.pgp', '')).encode('utf-8')
            response = gpg.decrypt_file(open(pgpfull_name, 'rb'),always_trust=True,passphrase=passphrase)
            if response.ok:
                with open(pfull_name, 'wb') as fpgp:
                    fpgp.write(response.data)
                return True
            else:
                return response.stderr
        except Exception as e:
            return e

    def decrypt(config_path,filename,path,DNS,inc_dt):
        try:
            bt = BaseTable(DNS)
            cfg_loaded = bt.load_configuration(config_path,path)
            bt.__config.log['Folder'] = path+bt.__config.log['Folder']
            bt.__config.log['FileNameFormat'] = path+bt.__config.log['FileNameFormat']
            logging = logWrapper.return_logging(bt.__config.log)

            end_time = time.time() + 1200 #3480  # time now + 1 hour
            logging.info('Searching for the file')

            # get the name of the file with date

            file_name = bt.searchFile(filename, bt.__config.input_folder,end_time,logging)

            # decrypt file
            new_file_name = file_name.replace('.pgp', '')
            dec = bt.pgp_decrypt(bt.__config.pgpexe,bt.__config.input_folder,bt.__config.output_folder,file_name,bt.__config.passphrase)
            if dec != True:
                logging.error(dec)
                sys.stdout.write('ERROR_DECRYPTING')

            # filename without date and with .csv
            full_path_file_name = os.path.join(bt.__config.output_folder, new_file_name)
            if ( not os.path.isfile(full_path_file_name) ) or os.path.getsize(full_path_file_name) < 1:
                logging.error('[!!] Error, File wasn\'t decrypted correctly')
                sys.stdout.write('ERROR_DECRYPTING')
                sys.exit(1)
            decrypted_file = bt.transfer_file(file_name,logging)  # file decrypted and in the right place

            logging.info('- Script moved the file')
            if inc_dt == '1':
                bt.include_date(bt.__config.output_folder, new_file_name,logging)
                
            #generating a new file with the date the file arrived
            """date_file = open('D:\\Globoforce_Extracts\\scripts\\SIT\\semaphore\\' + sys.argv[1] + '_date.csv','w')
            date_file.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            date_file.close()"""
                
            logging.info('[*] Script executed successfully!')
            sys.stdout.write('[*] Script executed successfully!')
        except Exception as e:
            print(e)
