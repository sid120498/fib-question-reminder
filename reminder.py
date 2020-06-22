#!/usr/bin/env python3
fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]

# !/usr/bin/python3

import pymysql
import datetime
import smtplib
FORMAT = '%Y-%m-%d'
now = datetime.datetime.now()
current_date = str(now.strftime('%Y-%m-%d'))
try:
    db = pymysql.connect("localhost", "root", "***", "fibonacci_reminder")
except:
    exit(0)
sql = "SELECT *  from questions \
      where send_at='%s'" % \
      current_date
cursor = db.cursor()
cursor.execute(sql)
rows = cursor.fetchall()
tobe_sent = []
for row in rows:
    cur_fib_item = int(row[4])
    id = int(row[5])
    send_at = datetime.datetime.strptime(row[2], FORMAT)
    tobe_sent.append([row[0], fib[cur_fib_item]])
    if cur_fib_item + 1 >= len(fib):
        continue
    next_send_at = str((datetime.datetime.now() + datetime.timedelta(days=fib[cur_fib_item + 1])).strftime(FORMAT))
    sql = "update questions set send_at='%s',fib_term=%d, last_sent='%s' \
          where id=%d" % (next_send_at, cur_fib_item + 1, current_date, id)
    cursor.execute(sql)

s = smtplib.SMTP('smtp.gmail.com', 587)

s.starttls()
s.login("***", "***")

# message to be sent
message = ""
for urls in tobe_sent:
    message = str(message)+str(urls[0])+'\t'+str(urls[1]) +'\n'
if(len(message)>0):
    message = 'Subject: {}\n\n{}'.format("Reminder", message)
    s.sendmail("***", "***", message)
    s.sendmail("****", "***", message)
#if failed above won't be commited
s.quit()
db.commit()
db.close()


