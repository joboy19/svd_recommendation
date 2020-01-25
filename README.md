# SVD Based Book Recommendation with REST Web System
Implementation of a SVD based recommendation systems using a modified version of the goodbooks-10k dataset.

To run:
```
python web_tech.py
```
The system will now be accessable at localhost:5000, provided you have flask installed.

Implementation uses SVD to decompose already recorded ratings for books to give users weights of latent factors 
which can be used to find the users which are the most similar to a new user and recommend books.
