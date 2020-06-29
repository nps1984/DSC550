import sys
from collections import OrderedDict
import pandas as pd
import numpy as np
import pprint


def create_dict_from_file(filename):
    """ Read in a file of itemsets
        each row is considered the transaction id
        and each line contains the items associated
        with it.
        This function returns a dictionary that
        has a key set as the tid and has values
        of the list of items (strings)
    """
    f = open(filename, 'r')
    d = {}
    for tids, line_items in enumerate(f):
        d[tids] = [j.rstrip("\n") for j in line_items.split(' ')
                   if j != '\n']
    return d


def create_database(itemset):
    "Uses dummy indexing to create the binary database"
    return pd.Series(itemset).str.join('|').str.get_dummies()


def compute_support(df, column):
    "Exploits the binary nature of the database"
    return df[column].sum()


def charm(itd, itlt, minsup, init_set):
    #### psuedo-code says to sort inside of charm. I sorted outside and passed it in. Is this ok?

    # loop through my itemset/transaction LIST
    for i, (i_col, i_tids) in enumerate(itlt):
        # create empty temporary holding set
        my_holding_dict = {}

        # loop through list again, but make sure we start AFTER the current element in our outer loop
        for j, (j_col, j_tids) in enumerate(itlt):
            if j <= i:
                continue
            else:
                # create a combined index ---------- if this isn't a set we get duplicate items in an itemset
                #ij_index = ''.join(sorted(set(i_col).union(j_col)))
                ij_intersection_items = set(i_col).intersection(j_col)
                set(j_col).difference_update(ij_intersection_items)

                #ij_index = ''.join(set(i_col).union(j_col))

                ij_index = str(i_col) + str(j_col)

                # generate interesection of transaction id's between current outer element and current inner element
                ij_t_list = list(set(i_tids).intersection(j_tids))

                # our support is the number of elements that intersected, if greater than our minimum support, move on
                if len(ij_t_list) >= minsup:

                    # if transactions are equal in outer element and current inner element
                    # replace outer element with combined index and original transaction ids
                    # add combined index and original transaction ids to temporary holding set
                    # remove inner element from outer list
                    if set(i_tids) == set(j_tids):

                        # replace key in dictionary with ij key but keep same values
                        itd[ij_index] = itd.pop(i_col)

                        # Add ij_index and i trans list to holding set
                        if i_col in my_holding_dict:
                            # replace key in dict if exists
                            my_holding_dict[ij_index] = my_holding_dict.pop(i_col)
                        else:
                            # if it doesn't exist, add list of tids for ij index
                            my_holding_dict[ij_index] = i_tids

                        # remove j key from dictionary
                        if j in itd:
                            del itd[j]

                        # set my iterator
                        i_col = ij_index
                    else:
                        # print(f"itids: {i_tids}")
                        # print(f"jtids: {j_tids}")

                        # if outer transactions are a subset of inner transactions
                        if set(i_tids).issubset(set(j_tids)):
                            # print("i is subset of j")

                            # replace key in dictionary with ij key but keep same values
                            itd[ij_index] = itd.pop(i_col)

                            # Add ij_index and i trans list to holding set
                            # my_holding_set.add((ij_index, i_tids))
                            if i_col in my_holding_dict:
                                # replace key in dict if exists
                                my_holding_dict[ij_index] = my_holding_dict.pop(i_col)
                            else:
                                # if it doesn't exist, add list of tids for ij index
                                my_holding_dict[ij_index] = i_tids

                            # set my iterator
                            i_col = ij_index
                        else:
                            # Add current itemset and transaction to holding dict
                            my_holding_dict[ij_index] = ij_t_list

        if len(my_holding_dict) > 0:
            # Recurse charm with holding set
            # convert holding set to list of tuples
            intermediate_lst_of_tuples = list(my_holding_dict.items())
            charm(my_holding_dict, intermediate_lst_of_tuples, minsup, init_set)

        already_closed = False
        for (z_itemset, z_tids) in init_set:
            if set(i_col).issubset(z_itemset) and set(i_tids) == set(z_tids):
                already_closed = True

        # if current itemset is not already closed, add it!
        if already_closed == False:
            init_set.append((i_col, i_tids))

if __name__ == '__main__':
    # Check if the command line arguments are given
    try:
        print('Filename: ', sys.argv[1])
        print('Min Support: ', sys.argv[2])
        pp = pprint.PrettyPrinter(indent=4)
    except:
        print('You need both a filename and a minimum support value!')

    minsup = int(sys.argv[2])

    # create dict of transaction ids and itemsets
    dict_itemset = create_dict_from_file(sys.argv[1])
    #pp.pprint(dict_itemset)

    # Create binary database based
    database = create_database(dict_itemset)

    # Create an empty list to hold frequent items
    freq_items = []

    # Check for freq items from binary database
    for col in database.columns:
        # compute support
        sup = compute_support(database, col)

        # Add tuple of column (item) and it's support if it is greater than our minsup
        if sup >= minsup:
            freq_items.append((col, sup))

    # create datatypes for structured array
    dtype = [('col', 'U3'), ('value', int)]
    #dtype = [('col', int), ('value', int)]

    # Use numpy array to store items
    a = np.array(freq_items, dtype=dtype)

    # sort aray based on indexes,
    a_sorted = np.sort(a, order=['value', 'col'])

    # create an empty list
    it_lst = []

    # for each item in array, loop
    for (itm, value) in a_sorted:
        # for each item, get the list of tranactions that item exists in
        # append to itm_tids list as a tuple
        it_lst.append((itm, database.loc[database[itm] == 1].index.tolist()))

    # Create ordered dictionary of my items and the transactions they exist in
    sorted_it_dict = OrderedDict(it_lst)

    # create an empty collection (list of tuples)
    my_final_set = []

    # P: item,transactions of item, P is sorted by support
    charm(sorted_it_dict, it_lst, minsup, my_final_set)

    # Loop through collection and print some info
    for (sorted_itm_tids, trans) in my_final_set:
        print(f"{sorted_itm_tids} - {len(trans)}")

    print(f"Total closed frequent itemsets: {len(my_final_set)}")
