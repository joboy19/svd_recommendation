import numpy as np 
import pandas as pd 
import random as random
import csv
from scipy.sparse.linalg import svds

k = 2


ratings = pd.read_csv("ratings copy.csv")
books = pd.read_csv("clean_test.csv")
#print(ratings.head())

rdf = ratings.pivot_table(index="user_id",columns="book_id",values="rating").fillna(0)
r = rdf.values
mean = np.mean(r, axis=1)
demean = r - mean.reshape(-1, 1)

print("input matrix")
print(r)

U, sigma, Vt = svds(demean, k=k)

print(U)
print(Vt)
sigma = np.diag(sigma)


vals = np.matmul(U, Vt) + mean.reshape(-1, 1)

VtS = np.matmul(sigma, Vt)
print(VtS)

#to get a prediction for a pre-existing user: get the values at vals[userID, book_ID]
#to get best predictions for a pre-existing user: find max of unseen values

newP = np.array([5,0,0,0,5])


new_person_value = np.matmul(newP, Vt)
print(new_person_value)

"""
for i in range(5):
    print(np.dot(newP, VtS[:,i:i+1]))
"""








