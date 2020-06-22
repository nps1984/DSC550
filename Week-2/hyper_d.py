import sys
import math
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
from statsmodels.distributions.empirical_distribution import ECDF


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


def compute_angle(point1, point2):
    return np.dot(point1, point2)/(np.linalg.norm(point1)*np.linalg.norm(point2))


def generate_all_angles(dimensions, pairs):
    results = np.zeros(pairs)
    for i in range(pairs):
        points = np.random.rand(2, dimensions)
        points[points<=0.5] = -1
        points[points>0.5] = 1
        results[i] = compute_angle(points[0], points[1])
    return results


def compute_angle(point1, point2):
    return np.dot(point1, point2) / (np.linalg.norm(point1) * np.linalg.norm(point2))


def generate_all_angles(d, pairs):
    results = np.zeros(pairs)
    for i in range(pairs):
        points = np.random.rand(2,d)
        points[points<=0.5] = -1
        points[points>0.5] = 1
        results[i] = compute_angle(points[0], points[1])
    return results

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
    vol_df.plot(x='dimension', y='volume')
    plt.xlabel('Dimension')
    plt.ylabel('Volume')
    plt.title('Hypersphere Volume')
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
    rad_df.plot(x='dimension', y='radius')
    plt.xlabel('Dimension')
    plt.ylabel('Radius')
    plt.title('Hypersphere Radius')
    #plt.show()

    ### Nearest Neighbors
    point_info = []

    for d in range(1,101):
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
    plt.xlabel('Dimension')
    plt.ylabel('Distance')
    plt.title('Nearest Neighbor Plot')
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

        if round(fraction_of_points,4) == 0:
            dim_essentially_0 = d

    fop_res = pd.DataFrame(fop)
    print(f'Dimension at which fraction is essentially 0 is {dim_essentially_0}')

    fop_res.plot(x="dimension", y="fraction")
    plt.xlabel('Dimension')
    plt.ylabel('Fraction')
    plt.title('Fraction of Points Inside Hypersphere')

    for d in range(1,2010, 10):
        thin_shell = volume_of_shell(r, ep, d)
        fop_ts.append({'dimension': d, 'fraction': thin_shell})

        if thin_shell >= 0.9999:
            dim_essentially_1 = d
            break

    fop_ts_res = pd.DataFrame(fop_ts)
    fop_ts_res.plot(x="dimension", y="fraction")
    print(f'Dimension at which fraction is essentially 1 is {dim_essentially_1}')
    plt.xlabel('Dimension')
    plt.ylabel('Fraction')
    plt.title('Fraction of Points Inside Thin Shell')
    #plt.show()

    ### Diagonals in High Dimensions
    pairs = 100000
    results = np.zeros(pairs)

    angles10 = generate_all_angles(10,pairs)
    angles100 = generate_all_angles(100, pairs)
    angles1000 = generate_all_angles(1000, pairs)
    ecdf10 = ECDF(angles10)
    ecdf100 = ECDF(angles100)
    ecdf1000 = ECDF(angles1000)

    fig10, ax10 = plt.subplots()
    ax10.plot(ecdf10.x,ecdf10.y)
    ax10.set_title('Dimensions of 10')
    ax10.set_xlable("Angle")
    ax10.set_ylable("Probability")

    fig100, ax100 = plt.subplots()
    ax100.plot(ecdf100.x, ecdf100.y)
    ax100.set_title('Dimensions of 100')
    ax100.set_xlable("Angle")
    ax100.set_ylable("Probability")

    fig1000, ax1000 = plt.subplots()
    ax1000.plot(ecdf100.x, ecdf100.y)
    ax1000.set_title('Dimensions of 1000')
    ax1000.set_xlable("Angle")
    ax1000.set_ylable("Probability")

    plt.show()