import numpy, scipy.sparse.linalg, random
from scipy.sparse import dok_matrix

X = dok_matrix((10000, 10000))
for i in range(10000):
    for j in range(10000):
        X[i,j] = random.uniform(0.0, 100.0)




print scipy.sparse.linalg.eigs(X, k = 4)
