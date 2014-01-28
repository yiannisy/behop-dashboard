#!/usr/bin/env python
import os,sys
import csv
from django.db import connection, transaction

fname=sys.argv[1]
table=sys.argv[2]

if __name__=='__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','behop_dashboard.settings')
    f = open(fname,'r')
    header_line = f.readlines()[0]
    cursor = connection.cursor()
    statement = "load data local infile '%s' into table %s character set latin1 fields terminated by ',' lines terminated by '\n' ignore 1 lines (%s) set timestamp=CONVERT_TZ(@timestamp,'-08:00','+00:00');" % (fname,table,header_line)
    cursor.execute(statement)
