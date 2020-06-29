import argparse
import pandas as pd
import numpy as np
from scipy.stats import multivariate_normal as mvn
from numpy.core.umath_tests import matrix_multiply as mm


def em_gmm_vect(xs, pis, mus, sigmas, tol=0.01, max_iter=100):

    n, p = xs.shape
    k = len(pis)

    ll_old = 0
    for i in range(max_iter):
        exp_A = []
        exp_B = []
        ll_new = 0

        # E-step
        ws = np.zeros((k, n))
        for j in range(k):
            ws[j, :] = pis[j] * mvn(mus[j], sigmas[j]).pdf(xs)
        ws /= ws.sum(0)

        # M-step
        pis = ws.sum(axis=1)
        pis /= n

        mus = np.dot(ws, xs)
        mus /= ws.sum(1)[:, None]

        sigmas = np.zeros((k, p, p))
        for j in range(k):
            ys = xs - mus[j, :]
            sigmas[j] = (ws[j,:,None,None] * mm(ys[:,:,None], ys[:,None,:])).sum(axis=0)

        sigmas /= ws.sum(axis=1)[:,None,None]

        # update complete log likelihoood
        ll_new = 0
        for pi, mu, sigma in zip(pis, mus, sigmas):
           ll_new += pi*mvn(mu, sigma).pdf(xs)

        ll_new = np.log(ll_new).sum()

        if np.abs(ll_new - ll_old) < tol:
            break
        ll_old = ll_new

    return ll_new, pis, mus, sigmas


def main():
    np.random.seed(123)

    # create data set
    n = 10
    _mus = np.array([[0,4], [-2,0]])
    _sigmas = np.array([[[3, 0], [0, 0.5]], [[1,0],[0,2]]])
    _pis = np.array([0.6, 0.4])
    xs = np.concatenate([np.random.multivariate_normal(mu, sigma, int(pi*n))
                        for pi, mu, sigma in zip(_pis, _mus, _sigmas)])

    # initial guesses for parameters
    pis = np.random.random(2)
    pis /= pis.sum()
    mus = np.random.random((2,2))
    sigmas = np.array([np.eye(2)] * 2)

    ll2, pis2, mus2, sigmas2 = em_gmm_vect(xs, pis, mus, sigmas)
    print(sigmas2)

if __name__ == '__main__':
    main()