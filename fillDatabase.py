import csv
import psycopg2

#conn_string contains all the needed settings for the database connection
conn_string = "host='localhost' dbname='election' user='postgres' password='postgres'"

conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

#Read Tweet Data and copy to database
#cursor.execute('''COPY tweet FROM '/Users/Kuzniarz/Documents/Bioinformatik Studium/SS 17/Datenbanken/Projekt/Neuer Ordner/aetDATA.csv' WITH DELIMITER ';' CSV HEADER''')

#Read Hashtag Data and copy to database
#cursor.execute('''COPY hashtag FROM '/Users/Kuzniarz/Documents/Bioinformatik Studium/SS 17/Datenbanken/Projekt/Neuer Ordner/aetTAGS.csv' WITH DELIMITER ';' CSV HEADER''')

#Read Hashtag Data and copy to database
cursor.execute('''COPY has FROM '/Users/Kuzniarz/Documents/Bioinformatik Studium/SS 17/Datenbanken/Projekt/Neuer Ordner/aetHas.csv' WITH DELIMITER ';' CSV HEADER''')

conn.commit();
