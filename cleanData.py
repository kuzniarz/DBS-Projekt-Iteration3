import csv
import re
import collections
from datetime import datetime

#These Strings contain all the file names
input_file = 'american-election-tweets.csv'
output_file = 'aetDATA.csv'
output_file_hashtags = 'aetTAGS.csv'

#defining order and name of fieldnames
fnames = ['id', 'handle', 'is_retweet', 'time', 'is_quote_status', 'retweet_count', 'favorite_count', 'text']

i = 0

#Help functions for data cleaning
#conerting a string to bool    
def str2bool(string):
    return string == 'True'

#fixing and finding all hashtags
def upperfind_hashtags(tweet):
    tweet.replace("# ", '#')
    tags = re.findall(r"#(\w+)", tweet)
    return [tag.upper() for tag in tags]

#creating timestamps out of strings
def time2stamp(string):
    return datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')

#removing non utf-8 symbols
def removeEmoji(string):
    string.encode('UTF-8', errors='ignore')
    #due to encoding there was a "b'" added to every text, but we fixed this with a little trick
    return string.replace("b'",'')

data=[]
with open(input_file, "r", errors='ignore') as f:
    reader = csv.reader(f, delimiter=';')
    next(reader) # skip the header
    for row in reader:
        # Format all the Data
        d = dict()
        d['id'] = i
        d['handle'] = row[0]
        d['is_retweet'] = str2bool(row[2])
        d['time'] = time2stamp(row[4])
        d['is_quote_status'] = str2bool(row[6])
        d['retweet_count'] = int(row[7])
        d['favorite_count'] = int(row[8])
        d['text'] = removeEmoji(row[1])
        d['hashtags'] = upperfind_hashtags(row[1])
        i = i + 1
        data.append(d)

#Writing csv file for tweets excluding hashtags because of external hashtag csv
with open(output_file, "w") as output:
    writer = csv.DictWriter(output, fieldnames=fnames, delimiter=';', extrasaction='ignore')
    writer.writeheader()
    for line in data:
        writer.writerow(line)
    
#print(data)

#creating hashtags set
hashtags = set()
for tweet in data:
    for h in tweet['hashtags']:
        hashtags.add(h)

#creating hashtag csv out of set
with open(output_file_hashtags, "w") as output:
    writer = csv.writer(output, delimiter=';')
    writer.writerow(["value","total_count"])
    #counting all occurences of tags 
    for element in sorted(hashtags):
        i=0
        for tweet in data:
            for l in tweet['hashtags']:
                if element==l:
                    i = i + 1
        writer.writerow([element,str(i)])
    
