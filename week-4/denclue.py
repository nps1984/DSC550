import argparse
import pandas as pd
import numpy as np
import scipy.linalg as la

def read_data(f1):
    return pd.read_csv(f1,header=None)


def findAttractor(x, D, h=0.1, e=1e-7):
    t = 0
    numeratorSum = 0
    denomSum = 0

    # init while loop iterable to large value
    point_diff = 100

    while point_diff <= e:
        xold = x.copy

        for i in range(D):
            numeratorSum += ((x - D[i])/h) * D[i]
            denomSum += ((x - D[i]) / h)

        # update x in place
        x = numeratorSum / denomSum
        t += 1

        point_diff = la.norm(x - xold)

    return x


def densityAttraction(xstar, D, h=0.1):
    kernel_sum = 0

    for i in range(D):
        kernel_sum += ((xstar - D[i])/h)
        return 1/(len(D)*h**D.shape[1])*kernel_sum

def denclue(data, h, min_thresh, eps):
    attractors = set()
    r_set_of_points = set()
    final_clusters = set()

    for x in data:
        x_star = findAttractor(x, data, h, eps)

        if densityAttraction(x_star, data, h) >= min_thresh:
            attractors.union(x_star)

            # we have vectors, so flatten them and then set them
            r_set_of_points.update(set(x_star.flatten()).union(x.flatten()))




if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("filename", help="File name to read dataset from")
    parser.add_argument("epsilon", type=float, default=.001, help="Value to check")
    args = parser.parse_args()

    # Pass argument to read data func to get a dataframe back
    df = read_data(args.filename)
    denclue()

    #eps, ll2, Ps, means, covs, iterations, points = em(df, args.clusters, args.epsilon)