import string
import sys
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import pandas as pd
import matplotlib.pyplot as plt
import pprint
import scipy.cluster.hierarchy as shc
from sklearn.cluster import KMeans



if __name__ == '__main__':

    # Exercise 7.2.2 - Show how different distances impact clustering
    data = np.array([[4, 10], [7, 10], [4, 8], [6, 8], [12, 6],
                     [10, 5], [11, 4], [3, 4], [9, 3], [12, 3], [2, 2], [5, 2]])

    # Create a cluster fit for each type of distance
    cluster1 = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='single')
    cluster1.fit_predict(data)

    cluster2 = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
    cluster2.fit_predict(data)

    cluster3 = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='average')
    cluster3.fit_predict(data)

    # Create plots for each cluster set
    f1 = plt.figure(1)
    dend1 = shc.dendrogram(shc.linkage(data, method='ward'))

    f2 = plt.figure(2)
    dend2 = shc.dendrogram(shc.linkage(data, method='average'))

    f3 = plt.figure(3)
    dend3 = shc.dendrogram(shc.linkage(data, method='single'))

    ### Excercise 7.3.4

    # Generate 3 clusters
    cluster = KMeans(3)

    # fit data to the clusters
    cluster.fit(data)

    # Get cluster centers
    print(f'Cluster centers:\n {cluster.cluster_centers_}\n')

    # Attach points to cluster and count
    cluster_label, counts = np.unique(cluster.labels_, return_counts=True)
    cluster_counts = dict(zip(cluster_label, counts))

    # cluster sums
    cluster_sums = {}

    for arr, lab in zip(data, cluster.labels_):
        if lab in cluster_sums:
            cluster_sums[lab] = np.add(cluster_sums[lab], arr)
        else:
            cluster_sums[lab] = arr

    # cluster sqsums
    cluster_sqsums = {}
    for arr, lab in zip(data, cluster.labels_):
        if lab in cluster_sqsums:
            cluster_sqsums[lab] = np.add(cluster_sqsums[lab], np.power(arr, 2))
        else:
            cluster_sqsums[lab] = np.power(arr, 2)

    # Variance & stdev
    cluster_vars = {}
    cluster_stds = {}
    for label in cluster_sums:
        cluster_vars[label] = cluster_sqsums[label] / cluster_counts[label] - np.power(
            cluster_sums[label] / cluster_counts[label], 2)

        cluster_stds[label] = np.sqrt(cluster_vars[label])

    # Print cluster info
    for label in cluster_counts:
        print(f'Point count for cluster {label}: {cluster_counts[label]}')
        print(f'Sum for cluster {label}: {cluster_sums[label]}')
        print(f'Sum of squares for cluster {label}: {cluster_sqsums[label]}')
        print(f'Cluster variancefor cluster {label}: {cluster_vars[label]}')
        print(f'Cluster STDEVfor cluster {label}: {cluster_stds[label]}\n')

    ### Exercise 7.3.5
    # A point
    p = np.array([[1, -3, 4]])

    # A cluster center
    c = np.array([[0, 0, 0]])

    # Standard deviations
    sigmas = np.array([[2, 3, 5]])

    # Mahalanobis distance
    print(f'Mahalanobis distance is: {np.sqrt((((c - p) / sigmas) ** 2).sum())}')

    # Show plots from 7.2.2
    plt.show()