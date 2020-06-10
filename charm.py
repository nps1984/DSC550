import sys
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


def charm(lst_o_tpls, minsup, init_set):
    # loop through list
    for i, (i_col, i_tids) in enumerate(lst_o_tpls):
        # print(f"i is {i}")

        # create empty temporary holding set
        my_holding_set = []

        # loop through list again, but make sure we start AFTER the current element in our outer loop
        for j, (j_col, j_tids) in enumerate(lst_o_tpls):
            # print(f"j is {j}")

            if i == j:
                continue
            elif j < i:
                continue
            else:
                # j > i
                # create a combined index
                ij_index = str(i_col) + str(j_col)

                # generate interesection of transaction id's between current outer element and current inner element
                t_list = list(set(i_tids).intersection(j_tids))

                # our support is the number of elements that intersected, if greater than our minimum support, move on

                if len(t_list) >= minsup:
                    #print(f't_list: {t_list}')

                    # print(f"new index: {ij_index}")
                    # print(f"t_list: {t_list}")

                    # if transactions are equal in outer element and current inner element
                    # replace outer element with combined index and original transaction ids
                    # add combined index and original transaction ids to temporary holding set
                    # remove inner element from outer list
                    if i_tids == j_tids:
                        # print("lists equal")
                        lst_o_tpls[i] = (ij_index, i_tids)

                        my_holding_set.append((ij_index, i_tids))
                        del lst_o_tpls[j]
                    else:
                        # print(f"itids: {i_tids}")
                        # print(f"jtids: {j_tids}")

                        # if outer transactions are a subset of inner transactions
                        if set(i_tids).issubset(set(j_tids)):
                            # print("i is subset of j")

                            # replace outer element with combined index and original transactions
                            # also replace current temporary holding set
                            lst_o_tpls[i] = (ij_index, i_tids)
                            # print(f"new list of tuples: {lst_o_tpls}")
                            # print(f"current holding set: {my_holding_set}")
                            # print(f"current icol: {i_col}")

                            # if we haven't added to the holding set yet, do it here
                            if len(my_holding_set) == 0:
                                my_holding_set.append((ij_index, t_list))
                            else:
                                # replace the holding set with the the combined index
                                (itm, trns) = my_holding_set[0]
                                tmp_index = str(itm) + str(j_col)
                                my_holding_set[0] = (tmp_index, trns)

                            # print(lst_o_tpls)
                            # print(my_holding_set)
                        else:
                            # print("i is NOT subset of j")
                            if len(my_holding_set) == 0:
                                my_holding_set.append((ij_index,t_list))
                                # print(f"adding init set to holding: {my_holding_set}")
                            else:
                                # property 3? I don't really understanding
                                (itm,trns) = my_holding_set[0]
                                unioned_trans = set(trns).union(set(t_list))
                                my_holding_set[0] = (itm,unioned_trans)

        if len(my_holding_set) > 0:
            # print(my_holding_set)
            # print('recurse charm')
            charm(my_holding_set, minsup, init_set)

        (itemset, trans_list) = lst_o_tpls[i]

        if len(trans_list) >= minsup:
            #if any(key.startswith(itemset) for key in init_set):
                init_set.append(lst_o_tpls[i])
                #init_set[itemset] = trans_list
        # print(f'init_set: {init_set}')

if __name__ == '__main__':
    # Check if the command line arguments are given
    try:
        print('Filename: ', sys.argv[1])
        print('Min Support: ', sys.argv[2])
        pp = pprint.PrettyPrinter(indent=4)
    except:
        print('You need both a filename and a minimum support value!')

    minsup = int(sys.argv[2])
    dict_itemset = create_dict_from_file(sys.argv[1])
    # pp.pprint(dict_itemset)

    database = create_database(dict_itemset)

    # Executes the brute force algorithm
    # NOTE: a list comprehension is faster

    freq_items = []
    for col in database.columns:
        freq = compute_support(database, col)
        a_tmp = (col, freq)
        freq_items.append((col, freq))

    # create structured array for sorting
    dtype = [('col', 'U3'), ('value', int)]
    #dtype = [('col', int), ('value', int)]
    a = np.array(freq_items, dtype=dtype)
    a_sorted = np.sort(a, order=['value', 'col'])

    col_tids = []
    for (col, value) in a_sorted:
        # tid_dict[col] = database.loc[database[col] == 1].index.tolist()
        #str_idx = str(col) + '|'
        col_tids.append((col + '|', database.loc[database[col] == 1].index.tolist()))

    my_final_set = []
    charm(col_tids, minsup, my_final_set)

    # Loop through collection and print some info
    for (itmst, trans) in my_final_set:
        print(f"{itmst} - {len(trans)}")

    print(f"Total closed frequent itemsets: {len(my_final_set)}")
