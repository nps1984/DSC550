import sys
import math
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from scipy.special import gamma


def get_factorial(x):
    return math.factorial(x)


def get_dbl_factorial(x):
    res = 1

    # start at x, go to -1, by decreasing 2
    for i in range(x, -1, -2):
        # return when i hits 0 or 1
        if (i == 0 or i == 1):
            return res
        else:
            # multiply current value to our previous result
            res *= i


def volume_of_hypersphere(r, d):
    numer = (math.pi) ** (d / 2)

    if d % 2 == 1:
        f = get_dbl_factorial(d)
        denom = ((f) / (2 ** ((d + 1) / 2))) * (math.sqrt(math.pi))
    else:
        denom = get_factorial(d / 2)

    return ((numer) / (denom)) * (r ** d)


def volume_of_hypercube(l, d):
    return l ** d


def volume_of_shell(r, ep, d):
    return 1 - (1- ep/r)**d


def get_radius(d,v):
    numer = (math.pi) ** (d / 2)

    if d % 2 == 1:
        f = get_dbl_factorial(d)
        denom = ((f) / (2 ** ((d + 1) / 2))) * (math.sqrt(math.pi))
    else:
        denom = get_factorial(d / 2)

    k = numer / denom
    r = (v/k)**(1/d)

    return r


if __name__ == '__main__':

    ### Hypersphere Volume
    # hardcode r value here
    r = 1

    # init empty list
    list_of_vols = []

    for d in range(1,51):
        volume = volume_of_hypersphere(r,d)
        list_of_vols.append({'radius': r, 'dimension': d, 'volume': volume})

    vol_df = pd.DataFrame(list_of_vols)
    plt.scatter(x=vol_df['dimension'],y=vol_df['volume'])
    #plt.show()

    ### Hypersphere Radius
    list_of_radii = []
    for d in range(1,101):
        VOLUME = 1
        radius = get_radius(d, VOLUME)
        list_of_radii.append({'radius': radius, 'dimension': d, 'volume': volume_of_hypersphere(radius,d)})
        # cal the volume function with radius and it shoudl return 1
        #print(f'radius: {radius}, dimension: {d}, and volume: {round(volume_of_hypersphere(radius,d),2)}')

    rad_df = pd.DataFrame(list_of_radii)
    plt.scatter(x=rad_df['dimension'], y=rad_df['radius'])
    #plt.show()

    ### Nearest Neighbors
    point_info = []

    for d in range(1,101):
        #center = np.full(d,.5)
        points = np.random.uniform(0, size=(10000, d))
        dist = cdist(points,np.expand_dims(np.full(d,.5),0),metric='euclidean')

        min_dist = np.amin(dist)
        max_dist = np.amax(dist)

        # index of max point
        min_point = np.where(dist == np.amin(dist))
        max_point = np.where(dist == np.amax(dist))

        point_info.append({'dimension':d,'ratio':min_dist/max_dist, 'nearest': min_dist, 'farthest': max_dist})

    near_neighbor_res = pd.DataFrame(point_info)
    near_neighbor_res.plot(x="dimension",y=["nearest","farthest"])
    #plt.show()

    ### Fraction of Volume
    fop = []
    fop_ts = []
    l = 2
    r = l / 2 # assumption based on p170
    ep = 0.01

    for d in range(1,101):
        points = np.random.uniform(0, size=(10000, d))
        sphere_vol = volume_of_hypersphere(r,d)
        cube_vol = volume_of_hypercube(l,d)

        fraction_of_points = sphere_vol / cube_vol # equation 6.18
        fop.append({'dimension':d,'fraction':fraction_of_points})

    fop_res = pd.DataFrame(fop)
    fop_res.plot(x="dimension", y="fraction")

    for d in range(1,2010, 10):
        thin_shell = volume_of_shell(r, ep, d)
        fop_ts.append({'dimension': d, 'fraction': thin_shell})

        if thin_shell >= 0.9999:
            print(f'BREAK! {d}')
            break

    fop_ts_res = pd.DataFrame(fop_ts)
    fop_ts_res.plot(x="dimension", y="fraction")

    plt.show()






