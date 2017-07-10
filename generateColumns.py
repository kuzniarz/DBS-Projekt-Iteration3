import psycopg2
import sys
from datetime import timedelta, date
import numpy as np
import matplotlib.pyplot as plt
import mpld3
import datetime

#conn_string contains all the needed settings for the database connection
conn_string = "host='localhost' dbname='election' user='postgres' password='postgres'"

conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
start_date = date(2016, 1, 5)
end_date = date(2016, 9, 30)
date = []
dayTags = []
hashCount = []
key = sys.argv[1]
print(key)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


for single_date in daterange(start_date, end_date):
    date.append(single_date.strftime("%Y-%m-%d"))

for n in range(len(date)-1):
    if (date[n] == "2016-09-30"):
        break
    else:
        valuelist = ""
        cursor.execute("""SELECT h.value FROM has as h, tweet as t WHERE t.id = h.id AND t.time BETWEEN %s AND %s""", (date[n] + "T00:00:00", date[n+1] + "T00:00:00"))
        for value in cursor:
            valuelist = valuelist + value[0];
        dayTags.append(datetime.datetime(int(date[n][:4]),int(date[n][5:-3]),int(date[n][-2:]),0))
        hashCount.append(str(valuelist.count(str(key))))

#Plotting given Data

ax = plt.subplot(111)
ax.bar (dayTags, hashCount, width=0.6, color='#0040FF')
ax.xaxis_date()
plt.xlabel("Tage")
plt.ylabel("Anzahl Hashtags")
if (str(key) == "#"):
    plt.title("Anzahl der Hashtags vom 05.01.2016 bis 30.09.2016 fuer alle Hashtags")
else:
    plt.title("Anzahl der Hashtags vom 05.01.2016 bis 30.09.2016 fuer " + str(key))
plt.grid(True)

fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

mpld3.save_html(fig, "./render/" + str(key) + "_render.html")

        