#Content filter
# import numpy as np
# import pandas as pd
# import csv
# from sklearn import preprocessing
# import warnings
# warnings.filterwarnings("ignore")
#
# trainset = pd.read_csv("processed-csv/IMDBMovieData.csv", encoding='latin-1')
#
# X = trainset.drop(['Title', 'ID', 'Votes', 'Year', 'Revenue','Metascore', 'Rating','Description', 'Runtime'], axis=1)
# #trainset.Revenue = X.Revenue.fillna(X.Revenue.mean())
# #trainset.Metascore= X.Metascore.fillna(X.Revenue.min())
# features = ['Genre','Actors','Director']
# for f in features:
#     X_dummy = X[f].str.get_dummies(',').add_prefix(f + '.')
#     X = X.drop([f], axis = 1)
#     X = pd.concat((X, X_dummy), axis = 1)
# # print (X.loc[5])
#
# #Ghi vào file testing
# y = list(X.columns.values)
#
# with open('testing.csv', 'w', encoding="ISO-8859-1") as test:
#        write = csv.writer(test, delimiter = ",")
#        write.writerow(['Content','Vote'])
#        for i in range(3030):
#            write.writerow([y[i]])
#
# # header = pd.read_csv("testing.csv")
# # header.shape
#
#
# #Xử lí file đã trích dẫn từ file movie, bao gồm các thuộc tính
# test = pd.read_csv("testing.csv")
#
# # print (test)
# T = test.drop(['Content'], axis=1)
# T = T['Vote'].fillna(0)
# vote = T.values
# vec = np.ones((1004,3026), dtype=np.uint8)
# vec = X.values
#
#
# sim = np.ones((1004,), dtype=np.complex_)
#
# for i in range (1,1004):
#     sim[i] = np.inner(vec[i],vote.transpose())
# print(sim.argsort())
# similar = sim.argsort()[::-1][:30]
# print ("ket qua---------------------------")
# print(similar)
# for i in range (30):
#     print (trainset.iloc[similar[i],1])
#


# #description
import re
import difflib
import pandas as pd
import numpy as np
import math
trainset = pd.read_csv("processed-csv/movies.csv", encoding='latin-1')
numlines = trainset.__len__()
input=13708
s1 = trainset.iloc[input,7]
s1w = re.findall('\w+', s1.lower())
sim = np.ones((numlines,), dtype=np.float)
for i in range (1,numlines):
    if i != input:
        s2 = trainset.iloc[i,7]
        if type(s2) == str :
            s2w = re.findall('\w+', s2.lower())
            common = set(s1w).intersection(s2w)
            common_ratio = 100*(difflib.SequenceMatcher(None, s1w, s2w).ratio())
            sim[i] = common_ratio
M = np.argmax(sim)
print ("your input movie is:",trainset.iloc[input,6])
print ("My suggestion for you is:",trainset.iloc[M,6])