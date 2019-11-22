import numpy as np 
import pandas as pd 
import random as random
import csv
from scipy.sparse.linalg import svds

k = 2


ratings = pd.read_csv("ratings copy 2.csv")
books = pd.read_csv("clean_test.csv")
#print(ratings.head())

rdf = ratings.pivot_table(index="user_id",columns="book_id",values="rating").fillna(0)
r = rdf.values
mean = np.mean(r, axis=1)
demean = r - mean.reshape(-1, 1)

print(r)

U, sigma, Vt = svds(demean, k=k)
sigma = np.diag(sigma)

#Vt = np.matmul(sigma, Vt)

vals = np.matmul(U, Vt) + mean.reshape(-1, 1)

#to get a prediction for a pre-existing user: get the values at vals[userID, book_ID]
#to get best predictions for a pre-existing user: find max of unseen values

newP = np.array([5,0,0,0,5])

print(newP)
print(U)
print(Vt)

newV = np.matmul(newP, Vt)


print(newV)









