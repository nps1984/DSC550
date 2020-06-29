import argparse
import pandas as pd
import numpy as np
from scipy.stats import multivariate_normal as mvn
from numpy.core.umath_tests import matrix_multiply as mm

def read_data(f1):
    return pd.read_csv(f1,header=None)


def random_val(column):
    """
    :param column:
    :return random number generated from min and max of column values:
    """

    minval = column.min()
    maxval = column.max()

    # Generate a random number from a uniform distribution of the min and max of the column.
    return np.random.uniform(minval,maxval,1)[0]


def em_init(df,k):
    # initialize a list for initial means
    # list of lists
    cluster_mus = []

    # initialize identiy matrix (4 elements for iris 4 attirbutes)
    init_sigmas = np.array([np.eye(4)] * k)

    # list of values
    init_cluster_probs = []

    ## xs = np.concatenate([np.random.multivariate_normal(mu, sigma, int(pi * n))
    ##                    for pi, mu, sigma in zip(_pis, _mus, _sigmas)])

    ### INITIALIZATION
    # for each cluster
    for i in range(k):

        # initialize mu
        attribute_mus = []

        # hardcoding loop for columns 0 through 3 in iris dataset
        for c in df[[0,1,2,3]]:
            attribute_mus.append(random_val(df[c]))

        # list of lists... list of each attribute mu for each clsuter.
        cluster_mus.append(attribute_mus)

        init_cluster_probs.append(1 / k)

    return np.array(cluster_mus),init_sigmas,init_cluster_probs


def em(df, k, eps):
    # init some values
    (mus, sigmas, probs) = em_init(df, k)

    n = len(df)
    ll_old = 0

    i = 0
    diff = 1
    while diff > eps and i < 1000000:
        ws = np.zeros((k, n))

        # for each cluster get posterior probability
        for j in range(k):
            ws[j, :] = probs[j] * mvn(mus[j], sigmas[j]).pdf(df.loc[:,0:3])
        ws /= ws.sum(0)

        #print(f'ws: {ws[0,:]}')
        #print(f'sums: {ws.sum(axis=1)}')
        # update probabilities
        probs = ws.sum(axis=1)
        probs /= n

        # update means
        mus = np.dot(ws, df.loc[:,0:3])
        mus /= ws.sum(1)[:, None]

        #print(mus)
        # update sigmas
        sigmas = np.zeros((k, 4, 4))

        for j in range(k):
            # get values from data frame, subtract mean values and convert to numpy array
            ys = (df.loc[:,0:3] - mus[j, :]).to_numpy()

            # Calculate sigmas using matrix multiply. gives a deprecation warning but couldn't figure it out with transpose
            sigmas[j] = (ws[j, :, None, None] * mm(ys[:, :, None], ys[:, None, :])).sum(axis=0)
        sigmas /= ws.sum(axis=1)[:, None, None]

        # init temporary log likelihood variable
        ll_new = 0

        # caclulate probability for each
        for p, mu, sigma in zip(probs, mus, sigmas):
            ll_new += p * mvn(mu, sigma).pdf(df.loc[:,0:3].to_numpy())

        ll_new = np.log(ll_new).sum()

        diff = np.abs(ll_new - ll_old)
        ll_old = ll_new

        # increment counter
        i += 1

    return diff, ll_new, probs, mus, sigmas, i, ws

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("filename", help="File name to read dataset from")
    parser.add_argument("clusters", type=int, default=3, help="How many clusters to create")
    parser.add_argument("epsilon", type=float, default=.001, help="Value to check")
    args = parser.parse_args()

    # Pass argument to read data func to get a dataframe back
    df = read_data(args.filename)

    eps, ll2, Ps, means, covs, iterations, points = em(df, args.clusters, args.epsilon)
    #print(eps,Ps, means, covs)
    #print(eps)
    #print(ll2)
    #print(Ps)
    #print(means)
    #print(covs)

    # for our probabilities of each cluster, create a dataframe
    cluster_points = pd.DataFrame()
    for nn, pp in enumerate(points):
        cluster_points[nn] = pp

    cluster_points['max_point'] = cluster_points.max(axis=1)
    cluster_points['cluster_assignment'] = cluster_points.idxmax(axis=1)


    #print(cluster_points.max(axis=1), cluster_points.idxmax(axis=1))
    #print(pd.DataFrame(points, columns=[0,1,2,3]))
    #$print(points[(points[0] > points[1]) & points[0] > points[2]])
    #(np.diff(np.vstack(points).reshape(len(points), -1), axis=0) == 0).all()

    for r,m in enumerate(means):
        print(f'The means for cluster {r} is {m}')

    for r,cvm in enumerate(covs):
        print(f'The covariance matrix for cluster {r} is\n {cvm}')

    print(f'The number of iterations until convergence was {iterations}')

    print(f"The number of points in each cluster is\n {cluster_points.groupby(['cluster_assignment']).agg('count')[0]}")

    #for r,cvm in enumerate(means):
    #    print(f'The covariance matrix for cluster {r} is {cvm}')

