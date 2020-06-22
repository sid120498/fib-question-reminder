#!/usr/bin/env python3

import pymysql
import datetime
from pathlib import Path

FILE_PATH = "/home/siddharthsing/PycharmProjects/fibonnaci-reminder/problemUrls.txt"

FORMAT = '%Y-%m-%d'
now = datetime.datetime.now()
created_date = str(now.strftime(FORMAT))
sent_at = now + datetime.timedelta(days=1)
sent_at = str(sent_at.strftime(FORMAT))
fib_term = 0
# Open database connection
try:
    db = pymysql.connect("localhost", "root", "****", "fibonacci_reminder")
except:
    exit(0)
urlFile = Path(FILE_PATH)
reminders = []
if urlFile.is_file():
    handle = open(FILE_PATH, 'r+')
    lines = handle.readlines()
    print(lines)
    for line in lines:
        line = line.strip()
        if len(line) > 5:
            line = line.split("|")
            url = "",
            complexity = "",
            comment = ""
            if len(line) > 0:
                url = line[0].strip()
            if len(line) > 1:
                complexity = line[1].strip()
            if len(line) > 2:
                comment = line[2].strip()
            reminders.append([url, created_date, sent_at, created_date, fib_term, complexity, comment])
    handle.truncate(0)
    handle.close()
else:
    exit(0)
if len(reminders) <= 0:
    exit(0)

sql = "INSERT INTO questions (url, \
   last_sent, send_at, created_at, fib_term, complexity, comment) \
   VALUES (%s, %s, %s, %s, %s, %s, %s )"
cursor = db.cursor()
cursor.executemany(sql, reminders)
db.commit()
db.close()
