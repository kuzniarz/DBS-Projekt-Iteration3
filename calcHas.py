import csv
import psycopg2

tags = []
tweets = []
hasList = []
edgeList = []
hashIDs = []

#variables
input_file = 'hashID.csv'
output_file = 'gephyTags.csv'
output_file_edges = 'gephyEdges.csv'
output_file_has = 'aetHas.csv'

#conn_string contains all the needed settings for the database connection
conn_string = "host='localhost' dbname='election' user='postgres' password='postgres'"

conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

#reading the hashIDs from .csv file
with open(input_file, "r") as f:
    reader = csv.reader(f, delimiter=',')
    next(reader) # skip the header
    for row in reader:
        hashIDs.append(row)

#function to get IDS for hashtags
def findID(hashtag):
    for elem in hashIDs:
        if (hashtag == elem[1]):
            return elem[0]

#SQL command for reading the hashtag values
cursor.execute("""SELECT value FROM hashtag""")
for value in cursor:
    tags.append([value[0]])

#SQL command to get needed tweet data    
cursor.execute("""SELECT id, text FROM tweet""")
for value in cursor:
    tweets.append([value[0], value[1]])

#calculates list for has table in postgresql    
for element in tweets:
    value = ""
    for hashtagA in tags:
         if ((element[1].upper().find("#"+hashtagA[0] + " ")) > -1):
            value = value + "#" + hashtagA[0]
            for hashtagB in tags:
                if ((element[1].upper().find("#"+hashtagB[0] + " ")) > -1) and hashtagA[0] != hashtagB[0]:
                    edgeList.append(findID(hashtagA[0]) + ";" + findID(hashtagB[0]))
    if (value == ""):
        value = "$"
    hasList.append([str(element[0]) + ";" + value])
        
#writes TAGS file for Gephi
with open(output_file, "w") as output:
    writer = csv.writer(output)
    writer.writerow("TAGS")
    for element in tags:
        writer.writerow(element)

#writes edges file for Gephi
with open(output_file_edges, "w") as output:
    writer = csv.writer(output)
    writer.writerow(["Source;Target"])
    for element in edgeList:
        writer.writerow([element])

#writes has file for postgresql
with open(output_file_has, "w") as output:
    writer = csv.writer(output)
    writer.writerow(["id;value;"])
    for element in hasList:
        writer.writerow(element)

    
