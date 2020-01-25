import numpy as np 
import pandas as pd 
import random as random
import csv
import math
from scipy.sparse.linalg import svds





#to get a prediction for a pre-existing user: get the values at vals[userID, book_ID]
#to get best predictions for a pre-existing user: find max of unseen values
#newP = newP - np.mean(newP)

k = 20

ratings = pd.read_csv("data/ratings.csv")
books = pd.read_csv("data/books.csv")
#print(ratings.head())

rdf = ratings.pivot_table(index="user_id",columns="book_id",values="rating").fillna(0)
r = rdf.values
mean = np.mean(r, axis=1)
demean = r - mean.reshape(-1, 1)
U, sigma, Vt = svds(demean, k=k)
sigma = np.diag(sigma)
Us = np.matmul(U, sigma)

print("Preprocessing done. (Calculated SVD, ready for recommendations)")


def get_books_total():
    re = csv.reader(open("data/books.csv", encoding='utf-8'))
    data = list(re)
    return len(data) - 1


def find_ratings(user_ID):
    user_ID = str(int(user_ID))
    out = np.zeros(get_books_total())
    count = 0
    with open("data/ratings.csv", "r", encoding='utf-8', newline='\n') as data1:
        for line in data1:
            data = line.rstrip().split(",")
            if data[0] == user_ID:
                count += 1
                out[int(data[1])-1] = int(data[2]) #book #1 is in index 0
    return out

#to get a prediction for a user, use the dataset as a starting point, run svd, matmul the new user to Vt
#  and calc euclidian distance from all vals in U
def make_prediction(user_ID):
    newP = find_ratings(user_ID)
    new_person_value = np.matmul(Vt, newP)

    closest_distance = 9999999
    closest_distance2 = 9999999
    closest_distance3 = 9999999

    closest_person = 0
    closest_person2 = 1
    closest_person3 = 2

    for x in range(len(Us)):
        if str(x+1) == user_ID:
            continue
        distance = np.linalg.norm(Us[x] - new_person_value)
        if distance < closest_distance:
            closest_distance3 = closest_distance2
            closest_distance2 = closest_distance
            closest_distance = distance
            closest_person3 = closest_person2
            closest_person2 = closest_person
            closest_person = x+1    #xth position in Us is the user with ID x+1
        elif distance < closest_distance2:
            closest_distance3 = closest_distance2
            closest_distance2 = distance
            closest_person3 = closest_person2
            closest_person2 = x+1
        elif distance < closest_distance3:
            closest_distance3 = distance
            closest_person3 = x+1


    ratings_x = find_ratings(str(closest_person))
    ratings_x2 = find_ratings(str(closest_person2))
    ratings_x3 = find_ratings(str(closest_person3))

    potential_books = []      
    for x in range(len(ratings_x)):
        if (ratings_x[x] != 0) and (newP[x] == 0):
            potential_books.append((x+1, ratings_x[x]))
    for x in range(len(ratings_x2)):
        if (ratings_x2[x] != 0) and (newP[x] == 0):
            potential_books.append((x+1, ratings_x2[x]))
    for x in range(len(ratings_x3)):
        if (ratings_x3[x] != 0) and (newP[x] == 0):
            potential_books.append((x+1, ratings_x3[x]))

    books = sorted(potential_books, key=lambda x: x[1])
    return [x[0] for x in books[:5]]
    



def get_book(id_):
    with open("data/books.csv", "r", encoding='utf-8', newline='\n') as data1:
        for line in data1: 
            data = line.rstrip().replace(", ", " ").replace("\"", "").split(",")
            if data[0] == id_:
                return data[1], data[2]
    return "False" 




def recommend_movies(predictions_df, userID, movies_df, original_ratings_df, num_recommendations=5):
    
    # Get and sort the user's predictions
    user_row_number = userID - 1 # UserID starts at 1, not 0
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)
    
    # Get the user's data and merge in the movie information.
    user_data = original_ratings_df[original_ratings_df.user_id == (userID)]
    user_full = (user_data.merge(movies_df, how = 'left', left_on = 'book_id', right_on = 'book_id').
                     sort_values(['rating'], ascending=False)
                 )
    print(user_full)
    
    # Recommend the highest predicted rating movies that the user hasn't seen yet.
    print(movies_df.head(10))
    recommendations = (movies_df[movies_df['book_id'].isin(user_full['book_id'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'book_id',
               right_on = 'book_id').
         rename(columns = {user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending = False).
                       iloc[:num_recommendations, :-1]
                      )

    return user_full, recommendations

