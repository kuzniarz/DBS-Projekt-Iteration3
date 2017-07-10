import psycopg2 as pg
import csv
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt, mpld3
from difflib import SequenceMatcher

a = []
i = 0
chordX = []
chordY = []
chordXY = []
data = []
clustering = []
output_file = "clusteringEdges.csv"

def alph2int(b):
    result = ord(b) - 26
    return result 
    
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def levenshtein(s, t):
        ''' From Wikipedia article; Iterative with two matrix rows. '''
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
                
        return v1[len(t)]

#conn_string contains all the needed settings for the database connection
conn_string = "host='localhost' dbname='election' user='postgres' password='postgres'"

conn = pg.connect(conn_string)
cursor = conn.cursor()

cursor.execute("""SELECT value FROM hashtag""")

for value in cursor:
    a.append([value[0]])

for tagA in a:
    levAdd = 0.0
    simAdd = 0.0
    for tagB in a:
        levAdd = levAdd + float(levenshtein(tagA[0],tagB[0]))
        simAdd = simAdd + float(similar(tagA[0], tagB[0]))
    chordX.append(simAdd/len(a))
    chordY.append(levAdd)
    chordXY.append([simAdd/len(a),levAdd])
    clustering.append(str(i) + ";" + str(tagA[0]) + ";" + str(round(simAdd/10, 4)) + ";" + str(round(levAdd/len(a), 4)))
    i = i + 1
        
cursor.close()
data = np.array(chordXY)

kmeans = KMeans(init='k-means++', n_clusters=6, random_state=0).fit(data)

labels = kmeans.labels_
centroids = kmeans.cluster_centers_

k = 3

for i in range(k):
    # select only data observations with cluster label == i
    ds = data[np.where(labels==i)]
    # plot the data observations
    plt.plot(ds[:,0],ds[:,1],'o', markersize=4)
    # plot the centroids
    lines = plt.plot(centroids[i,0],centroids[i,1],'kx')
    # make the centroid x's bigger
    plt.setp(lines,ms=15.0)
    plt.setp(lines,mew=2.0)

mpld3.save_html(plt.gcf(), "kmeans_render.html")

with open(output_file, "w") as output:
    writer = csv.writer(output)
    writer.writerow(["Id;Value;Dimension 1;Dimension 2"])
    for element in clustering:
        writer.writerow([element])
