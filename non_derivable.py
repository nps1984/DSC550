import sys

def create_dict_from_file(filename):
    f = open(filename, 'r')
    d = {}
    for lines in f:
        k,v = [j.rstrip("\n") for j in lines.split(' - ') if j != '\n']
        fznset = frozenset(k.split(' '))
        d[fznset] = int(v)

    return d


def create_itemsets_from_file(filename):
    f = open(filename, 'r')
    los = []
    for lines in f:
        tl = [j.rstrip("\n") for j in lines.split(' ') if j != '\n']
        los.append(set(tl))
    return los


def power_set(A):
    """ Compute all subsets of a given set """
    length = len(A)
    return {
        frozenset({e for e, b in zip(A, f'{i:{length}b}') if b == '1'})
        for i in range(2 ** length)
    }


def compute_gen_item_support(y, W, ds):
    """ Compute generalized itemset support """
    sup_y_barz = 0

    # for each subset in powerset of current itemset
    for w in W:
        # if y is a subset of current subset
        if y.issubset(w):
            coef=(-1)**len(w.difference(y))
            w_sup = ds[w]
            sup_y_barz += (coef*w_sup)

    return sup_y_barz


def compute_bound(x, y, W, ds):
    """Calcuate a boundry based on supports of all subsets of our current itemset

     Keyword arguments:
         x -- the current itemset
         y -- the current subset of the itemset
         W -- the powersets of x
         ds -- dictionary of support values from input file
     """
    # init bound value
    bound = 0

    # for each subset of our itemset, loop
    for w in W:
        # if current subset is our itemset, skip it
        if x == w:
            continue
        # if y is a subset of current subset or y is empty, compute bound
        elif y.issubset(w) or len(y)==0:
            # determine coefficient value
            coef = (-1) ** (len(x.difference(w)) + 1)

            # check for length of w because if y is empty then w could be empty, handle that in thelse
            if (len(w) > 0 ):
                # get the support of the current subset of our itemset
                w_sup = ds[w]
            # if y is the empty set, use our itemset to get support
            else:
                # convert x to a frozenset to access key/value from our dictionary
                fznset = frozenset(x)
                w_sup = ds[fznset]

            # bound is summation of coefficient multiplied by support
            bound += (coef * w_sup)

    # return bound
    return bound

if __name__ == '__main__':
    # Check if the command line arguments are given
    try:
        print('Supports Filename: ', sys.argv[1])
        print('Itemsets Filename: ', sys.argv[2])
    except:
        print('You need to provide two filenames!')

    # this creates a dictionary using the itemsets as keys and the supports as values
    dict_sups = create_dict_from_file(sys.argv[1])

    # creates a list of sets for each itemset
    list_of_itemsets = create_itemsets_from_file(sys.argv[2])

    # loop through each itemset in the ndi.txt file
    for x in list_of_itemsets:
        # get all subsets of the current itemset
        all_ys = power_set(x)

        # init lower and upper bounds, including 0 in lower bound
        lb = {0}
        ub = set({})

        # loop through each subset of current itemset
        for y in all_ys:
            # if our current itemset and our current subset are equal, we can skip it
            if x == y:
                continue

            # computer X \ Y
            z = x.difference(y)

            # if even, computer bound and add to lower bound set
            if (len(z) % 2) == 0:
                lb.add(compute_bound(x,y,all_ys,dict_sups))
            # if odd, computer bound and add to upper bound set
            else:
                ub.add(compute_bound(x,y,all_ys,dict_sups))

        # compare max in lower bound set to min in upper bound set, and set variable
        if max(lb) != min(ub):
            is_derivable = 'nonderivable'
        else:
            is_derivable = 'derivable'

        # print info about our current itemset
        print(f'Itemset {x} lb:{sorted(lb)},ub:{sorted(ub)} - {is_derivable}')

