import numpy as np 
import pandas as pd 
import random as random
import csv
from scipy.sparse.linalg import svds


ratings = pd.read_csv("ratings.csv")
books = pd.read_csv("clean_test.csv")
#print(ratings.head())

rdf = ratings.pivot_table(index="user_id",columns="book_id",values="rating").fillna(0)
r = rdf.values
mean = np.mean(r, axis=1)
demean = r - mean.reshape(-1, 1)

U, sigma, Vt = svds(demean, k=50)
sigma = np.diag(sigma)




