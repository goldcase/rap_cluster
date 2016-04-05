import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import KMeans
from random import shuffle

import os, cPickle

PROCESSED_DATA_DIR = "processed_data"

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
def get_data():
    ret = []
    vec = DictVectorizer()

    dirs_list        = next(os.walk(PROCESSED_DATA_DIR))[1]
    joined_dirs_list = [os.path.join(PROCESSED_DATA_DIR, d) for d in dirs_list]

    for subdir in joined_dirs_list:
        # Walk files in every subdirectory.
        for root, dirs, files in os.walk(subdir):
            for file_item in files:
                file_path = os.path.join(subdir, file_item)

                # Read file and vectorize lyrics.
                with open(file_path) as f:
                    ret.append(cPickle.load(f))

    return vec.fit_transform(ret).toarray()

data = get_data()
print data

estimator = KMeans(n_jobs=-1)
estimator.fit(data)

# Verify center clusters are around 25 and 10.
print(estimator.cluster_centers_)

