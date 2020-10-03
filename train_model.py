import numpy as np
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
import pickle
iris_X, iris_y = datasets.load_iris(return_X_y=True)
np.unique(iris_y)
np.random.seed(0)
# Create and fit a nearest-neighbor classifier
knn = KNeighborsClassifier()
knn.fit(iris_X, iris_y)

with open('knn.pkl', 'wb') as pickle_file:
    pickle.dump(knn, pickle_file)