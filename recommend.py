# Content based movie recommender system
# References and credits at bottom

# imports
import pandas as pd
import numpy as np
import time
import sys
import os
import itertools

from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# function definitions
def get_title(index):
    return df[df.index == index]["title"].values[0]

def get_index(title):
    return df[df.title == title]["index"].values[0]

def combine(row):
    return row["keywords"]+" "+row["genres"]+" "+row["director"]+" "+row["cast"]

try:
    # Loading CSV and doing some string operations
    df = pd.read_csv(os.path.dirname(__file__)+"/dataset/movie_dataset.csv")
    df["title"] = df["title"].str.upper()

    # Cleaning up the data 
    features = ["keywords", "genres", "director", "cast"]
    for feature in features:
        df[feature]=df[feature].fillna(" ")

    # Creating new df with only the selected relevant features 
    df["combined"] = df.apply(combine, axis=1)

    # Creating the count matrix and using fit and transform method
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined"])
    # Using cosine similarity as the basis of recommendations
    cosine_sim = cosine_similarity(count_matrix)
    # Menu for selecting movies and getting recommendations 
    print("Starting Program.....", end = " ")
    spinner = itertools.cycle(["|", "/", "-", "\\"])
    for i in range(25):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b")
    print()
    print("\nMovie Recommendation Engine (Content Based)")
    while True:
        usrmovie = input("\nPlease enter a movie that you like: ")
        usrmovie = usrmovie.upper()
        for i in tqdm(range(100), desc="Loading recommendations for you"):
            time.sleep(0.015)
        
        try:
            index = get_index(usrmovie)
            # Creating a list of tuples of movies from the count matrix for given movie index
            recommended_movies = list(enumerate(cosine_sim[index]))
            # Sorting the list in descending order
            sorted_recommendations = sorted(recommended_movies, key = lambda x:x[1], reverse = True)
            # Displaying top 25 similar movies
            print("\nHere are the top 25 movies we recommend based on your choice: ")
            # Counter for 25
            i = 0
            for movie in sorted_recommendations:
                if get_title(movie[0])==usrmovie:
                    pass
                else: 
                    print(get_title(movie[0]))
                    i+=1
                    if i==10:
                        break
        except:
            # Returning error if there is no data of the movie in csv file
            print("\nSorry we couldn't find recommendations for {}, please try another movie.".format(usrmovie))
        # Option to continue going through the program or quit
        while True:    
            inp = input("Do you want to continue finding recommendations? (y/n): ")
            inp.casefold()
            if inp == "n" or inp == "no":
                print("User selected \"no\", Terminating!.....")
                flag = 0
                break
            elif inp == "y" or inp == "yes":
                flag = 1
                break
            else:
                print("Invalid input please enter y or n.")
        #Flag check to find out what user selected
        if flag == 1:
            continue
        elif flag == 0:
            break
        #Error message (just in case)
        else:
            print("Fatal error! Terminating....")
            break

except KeyboardInterrupt:
    print("\nSIGTERM received terminating...")



    # References: 
    # Code Heroku YouTube Channel 
    # Documentation of libraries and modules used
    # Dataset downloaded from https://notebooks.azure.com/hello-codeheroku/projects/recommendation-systems/html/movie_dataset.csv