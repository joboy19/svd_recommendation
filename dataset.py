import csv
import random as r

## want to chop the book dataset and the rating dataset
## need to remove books and ratings for those books

def delete_ratings(bookids):
    r = csv.reader(open("data/ratings.csv"))
    data = list(r)
    out = []
    for x in range(len(data)):
        if data[x][1] in bookids:
            out.append(data[x])
    writer = csv.writer(open('data/ratings.csv', 'w', newline='\n', encoding='utf-8'))
    writer.writerows(out)

def delete_books():
    re = csv.reader(open("data/books.csv", encoding="utf-8"))   
    data = list(re)
    out = []
    outIDs = []
    for x in range(len(data)):
        if r.random() < 0.125:
            bookid = data[x][0]
            outIDs.append(bookid)
            out.append(data[x])
    writer = csv.writer(open('data/books.csv', 'w', newline='\n', encoding='utf-8'))
    writer.writerows(out)
    delete_ratings(outIDs)

def fix_books():
    re = csv.reader(open("data/books.csv", encoding="utf-8")) 
    data = list(re)
    re2 = csv.reader(open('data/ratings.csv', newline='\n', encoding='utf-8'))
    data2 = list(re2)
    mapping = []
    for x in range(1, len(data)):
        mapping.append(int(data[x][0]))
    mapping = sorted(mapping)
    print(mapping)
    for x in range(1, len(data)):
        data[x][0] = str(mapping.index(int(data[x][0])) + 1)
    for x in range(1, len(data2)):
        data2[x][1] = str(mapping.index(int(data2[x][1])) + 1)

    writer = csv.writer(open('data/books.csv', 'w', newline='\n', encoding='utf-8'))
    writer.writerows(data)
    writer = csv.writer(open('data/ratings.csv', 'w', newline='\n', encoding='utf-8'))
    writer.writerows(data2)

def fix_ratings():
    re = csv.reader(open("data/ratings.csv", encoding="utf-8")) 
    data = list(re)
    mapping = set()
    for x in range(1, len(data)):
        mapping.add(int(data[x][0]))
    mapping = list(mapping)
    for x in range(1, len(data)):
        data[x][0] = str(mapping.index(int(data[x][0])) + 1)
    writer = csv.writer(open('data/ratings.csv', 'w', newline='\n', encoding='utf-8'))
    writer.writerows(data)


