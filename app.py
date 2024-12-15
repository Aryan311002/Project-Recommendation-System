import streamlit as st
import requests
import pandas as pd
import pickle

st.title("Books You'ld Love to read!")

book = st.text_input("Enter a book name")

with open('recommender_system\sim_test.pkl', 'rb') as file:
  sim_test = pickle.load(file)

response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={book}")
data = response.json()

list_of_books = []
image_links = []

for i in range(len(data["items"])):
    list_of_books.append(data["items"][i]["volumeInfo"]["title"])
    image_links.append(
        data.get("items", [{}])[i]
        .get("volumeInfo", {})
        .get("imageLinks", {})
        .get("smallThumbnail")
    )


df = pd.DataFrame({"title": list_of_books, "link": image_links})

button = st.button("Read")

if button:

    if book in df["title"].values:

        print("book in df")
        idx = df[df["title"] == book].index[0]
        sim_scores = sorted(
            list(enumerate(sim_test[idx])), key=lambda x: x[1], reverse=True
        )
        print(sorted(list(enumerate(sim_test[idx])), key=lambda x: x[1], reverse=True))
        first_elements = [item[0] for item in sim_scores]
        suggestions = df.iloc[first_elements]['title']
        
        st.dataframe(suggestions)

    else:
        print("Book not found in the dataset.")
        print(df["title"])
        st.subheader("Book Not Found")
