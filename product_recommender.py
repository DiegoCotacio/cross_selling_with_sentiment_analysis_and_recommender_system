import pickle
import numpy as np

class BookRecommender:
    def __init__(self, model, book_names, final_rating, book_pivot):
        self.model = pickle.load(open(model, 'rb'))
        self.book_names = pickle.load(open(book_names, 'rb'))
        self.final_rating = pickle.load(open(final_rating, 'rb'))
        self.book_pivot = pickle.load(open(book_pivot, 'rb'))

    def recommend_book1(self, selected_book):
        book_id = np.where(self.book_pivot.index == selected_book)[0][0]
        distance, suggestion = self.model.kneighbors(self.book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

        recommend_list = []
        for i in range(len(suggestion)):
            books = self.book_pivot.index[suggestion[i]]
            for j in books:
                recommend_list.append(j)

        return recommend_list