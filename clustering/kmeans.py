import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import argparse


def read_data(f1):
    return pd.read_csv(f1,header=None)


def getvalues(df, start, stop):
    """
    Slice column data from dataframe
    :param df: input dataframe
    :param start: which column to start with
    :param stop: which column to stop at
    :return: numpy array of values
    """

    return df.iloc[:, start:stop].values


def runKMeans(num_clusters):
    pass


def findElbow(d, Klusters):
    """
    Take in a data set and determine the optimal number of clusters
    :param d: data set
    :param Klusters: max number of clusters
    :return:  a list of inertias (sum of squared distances)
    """

    inertias = []
    for k in range(1,Klusters):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)

    return inertias


def findGap(d,Klusters, Refs):
    """
    Using kmeans, find the gap statistic of a data set
    :param d: data set
    :param Klusters: max number of clusters
    :param Refs: Number of reference sets to generate
    :return: A dataframe containing the cluster count and the gap score
    """
    results = pd.DataFrame({'clusters': [], 'gap': []})

    # Loop until our max number of clusters
    for g, k in enumerate(range(1, Klusters)):

        # Create an array to hold our reference data points
        referenceDataPoints = np.zeros(Refs)

        # generate random sample and perform kmeans on that sample
        for r in range(Refs):
            # get a uniform random sampling the same size as our data
            randomRef = np.random.uniform(0, 1, d.shape)

            # fit a model on the random sampling of data
            rm = KMeans(k)
            rm.fit(randomRef)

            # add sum of squares information to our reference df
            refDP = rm.inertia_
            referenceDataPoints[r] = refDP

        # fit cluster on original data set
        om = KMeans(k)
        om.fit(data)

        # Get sum of square info
        orgDP = om.inertia_

        # Calculate gap between reference and original data sets
        gap = np.log(np.mean(referenceDataPoints)) - np.log(orgDP)

        # Update array with gap score
        results = results.append({'clusters': k, 'gap': gap}, ignore_index=True)

    return results



if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Process inputs for kmeans clustering against iris data set.')
    parser.add_argument("filename", help="File name to read dataset from")
    parser.add_argument("max", type=int, default=10, help="Max iterations to perform")
    parser.add_argument("ref", type=int, default=3, help="How many references to create for gap statistic")

    args = parser.parse_args()

    # Pass argument to read data func to get a dataframe back
    df = read_data(args.filename)
    data = getvalues(df,0,4)

    # Find elbow
    inertias = findElbow(data, args.max+1)

    for i,sse in enumerate(inertias):
        print(f'Cluster {i+1}:\t{sse}')

    plt.plot(range(1,args.max+1), inertias, linewidth=3)
    plt.grid(True)
    plt.xlabel('Cluster Count')
    plt.ylabel('SSQ Value')
    plt.title('SSQ by Cluster Count')
    plt.show()

    # Find gap statistic
    for r in [args.ref, args.ref*2]:
        gaps = findGap(data, args.max+1, r)

        print(f'Gaps for ref value: {r}')
        print('-'*40)

        for i,gap in enumerate(gaps['gap']):
            print(f'Cluster {i+1}:\t{gap}')

        plt.plot(gaps['clusters'], gaps['gap'], linewidth=3)
        plt.xlabel('Cluster Count')
        plt.ylabel('Gap Value')
        plt.title('Gap Values by Cluster Count')
        plt.show()

    print(f'For the elbow, the value of k is typically estimated at 3. For the gap statistic, it is typically 8.')
    print(f'The elbow estimates are consistently close to the number of species. The gap is usually higher')
    print(f'In this case, the elbow seems to be more consistent for generating optimal number of clusters.')
