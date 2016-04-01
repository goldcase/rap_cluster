import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from random import shuffle

# K Means attempts to cluster data by splitting data into groups of equal variance.
# Requires number of clusters to be specified.
# Centroid: mean of cluster.
# Aims to choose centroids that minimize the inertia, or intra-cluster sum of squared distance from the mean.

# Drawbacks
# Note that inertia makes the assumption that clusters are convex and isotropic (identical in all directions).
# Inertia responds poorly to elongated clusters.
# Inertia is not a normalized metric. PCA can reduce the inflation of Euclidean distances that occur with high-dimensional spaces.
# 1. Choose initial centroid, k samples from the dataset.
# 2. Assign each sample to its nearest centroid
# 3. Create new centroids by taking the mean value of all the samples assigned to each previous centroid.
# K means will always converge, but this might be a local minimum, heavily dependent on centroid initialization.
# As such, centroid initialization is done several times.

# In other words, k-means is EM w/small, all-equal diagonal covar matrix.

estimator = KMeans()
estimator.fit(data)

# Verify center clusters are around 25 and 10.
print(estimator.cluster_centers_)

# Plot actual, generated values.
plt.figure(0)
plt.scatter(x_vals_c1, y_vals_c1, color='r')
plt.scatter(x_vals_c2, y_vals_c2, color='b')
plt.show()

cluster_1 = []
cluster_2 = []

# Split the labeled points into cluster 1, cluster 2.
for i, v in enumerate(estimator.labels_):
    if v:
        cluster_1.append(data[i])
    else:
        cluster_2.append(data[i])

# Plot the two clusters in different colors. Christmas-themed.
plt.figure(1)
plt.scatter(*zip(*cluster_1), color='g')
plt.scatter(*zip(*cluster_2), color='r')
plt.show()
