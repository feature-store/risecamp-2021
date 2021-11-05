import pandas as pd
import numpy as np
import csv

n_users = 610
n_movies = 193609

def read_csv(filename):
    data = dict()
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for r in reader:
            data.append([float(j) for j in r])
    return np.array(data)

def create_split(stream_df):
    columns = ["userId", "movieId", "rating"]
    test_data = np.zeros((n_users, n_movies))
    data = []
    for userId in stream_df["userId"].unique():
        user_df = stream_df[stream_df["userId"] == userId]
        random_five = user_df.sample(5)
        for row in user_df.itertuples():
            if any(random_five["movieId"] == row.movieId):
                test_data[row.userId - 1, row.movieId - 1] = row.rating
            else:
                data.append([row.userId, row.movieId, row.rating])
    train_df = pd.DataFrame(data=data, columns=columns)
    return test_data, train_df

class ALSModel:
    def __init__(self, l):
        self.l = l
        self.num_features = 20
        self.movie_matrix = read_csv("movie_matrix.csv")
        self.ratings = dict()
        self.user_matrix = dict()
    
    def als_step(self, userId, movieId, rating):

        if userId in self.user_matrix:
            user_vector = self.user_matrix[userId]
            rating_vector = self.ratings[userId]
        else:
            user_vector = np.random.randint(100, size=(1, self.num_features))
            rating_vector = np.zeros((1, n_movies))
        
        rating_vector[0, movieId-1] = rating
        updated_user_vector = self._als_step(rating_vector, user_vector, self.movie_matrix)
        self.user_matrix[userId] = updated_user_vector
        self.ratings[userId] = rating_vector

    def predict(self, userId, movieId):
        user_vector = self.user_matrix[userId] 
        movie_vector = self.movie_matrix[movieId - 1]
        return user_vector.dot(movie_vector.T)

        
    def _als_step(self, ratings, solve_vecs, fixed_vecs):
        """
        when updating the user matrix,
        the item matrix is the fixed vector and vice versa
        """
        A = fixed_vecs.T.dot(fixed_vecs) + np.eye(self.num_features) * self.l
        b = ratings.dot(fixed_vecs)
        A_inv = np.linalg.inv(A)
        solve_vecs = b.dot(A_inv)
        return solve_vecs
    
    @staticmethod
    def compute_mse(y_true, y_pred):
        """ignore zero terms prior to comparing the mse"""
        mask = np.nonzero(y_true)
        mse = mean_squared_error(y_true[mask], y_pred[mask])
        return mse
        