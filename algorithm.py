import os
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_most_similar_file(response_as_query, docx_dir):
    # Load all docx files as strings and store in a list
    docx_texts = []
    for filename in os.listdir(docx_dir):
        if filename.endswith(".docx"):
            file_path = os.path.join(docx_dir, filename)
            text = docx2txt.process(file_path)
            docx_texts.append(text)

    # Create a tf-idf vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the docx texts and query text
    docx_tfidf = vectorizer.fit_transform(docx_texts)
    query_tfidf = vectorizer.transform([response_as_query])

    # Calculate the cosine similarities between the query and all docx texts
    similarities = cosine_similarity(query_tfidf, docx_tfidf)[0]

    # Get the index of the most similar docx text
    most_similar_index = similarities.argmax()

    # Get the file name of the most similar docx text
    most_similar_filename = os.listdir(docx_dir)[most_similar_index]

    return most_similar_filename




# to call the above function
"""
docx_dir = "/content/sample_data"
query = input("enter something")
most_similar_filename = find_most_similar_file(docx_dir, query)
print("The most similar file is:", most_similar_filename)"""


"""I think we should take chatbot respomse as a query for this alogorithm /  
take the user input i.e is question from user as input for the alogrithm ----> find the best one to get accurate output"""