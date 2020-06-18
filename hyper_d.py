import sys
import math
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
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


def getPoint() {
    var u = Math.random();
    var v = Math.random();
    var theta = u * 2.0 * Math.PI;
    var phi = Math.acos(2.0 * v - 1.0);
    var r = Math.cbrt(Math.random());
    var sinTheta = Math.sin(theta);
    var cosTheta = Math.cos(theta);
    var sinPhi = Math.sin(phi);
    var cosPhi = Math.cos(phi);
    var x = r * sinPhi * cosTheta;
    var y = r * sinPhi * sinTheta;
    var z = r * cosPhi;
    return {x: x, y: y, z: z};
}
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
    for d in range(1,11):
        np.random.uniform(0,1,10000)