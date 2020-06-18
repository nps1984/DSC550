import string
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pprint


def jaccard_similarity(l1, l2):
    s1 = set(l1)
    s2 = set(l2)

    intersection = len(list(set(l1).intersection(l2)))
    union = len(list(set(l1).union(l2)))

    return round(intersection/union,4)


def gen_stop_words(sentence, size):
    # remove punctuation from sentence
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))

    # create an empty list
    #stop_words_list = []

    # list comprehension to split sentence into words and generate stop words if they are less than noted size
    # initially converted all case to lower
    #[stop_words_list.append(str(word).lower()) for word in sentence.split() if len(word) <= size and str(word).lower() not in stop_words_list]

    #[stop_words_list.append(str(word)) for word in sentence.split() if len(word) <= size and str(word) not in stop_words_list]
    stop_words = {str(word) : 1 for word in sentence.split() if len(word) <= size}

    # Return my list of stop words
    return stop_words


def get_shingles(sentence, stop_words, shingle_size):
    # remove punctuation again
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))

    # create a list of words
    words = sentence.split()

    # Empty list to hold my shingles
    shingles = []

    # List comprehension to add shingles to a list
    [shingles.append(words[i:i + shingle_size]) for (i, word) in enumerate(words) if word in stop_words.keys() and len(words[i:i + shingle_size]) == shingle_size ]

    # Return my shingles
    return shingles


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
           d[tids] = [j.rstrip('\n') for j in line_items.split(' ')
                           if j != '\n']
    return d


def compute_minhash_sigs(database):
    sig_matrix = pd.DataFrame(np.inf, index=['h1','h2','h3'], columns=database.columns)
    indexes = database.index.tolist()

    h1 = []
    h2 = []
    h3 = []

    for i in indexes:
        i = int(i)
        h1.append(((2 * i) + 1) % 6)
        h2.append(((3 * i) + 2) % 6)
        h3.append(((5 * i) + 1) % 6)

    #database['h1'] = h1
    #database['h2'] = h2
    #database['h3'] = h3
    hf = pd.DataFrame({'h1':h1, 'h2':h2, 'h3':h3})

    for (index, row) in database.iterrows():
        index = int(index)
        for col, val in row.items():
            if val == 1:
                if hf.at[index,'h1'] < sig_matrix.at['h1',col]:
                    sig_matrix.at['h1',col] = hf.at[index,'h1']
                if hf.at[index, 'h2'] < sig_matrix.at['h2', col]:
                    sig_matrix.at['h2', col] = hf.at[index, 'h2']
                if hf.at[index, 'h3'] < sig_matrix.at['h3', col]:
                    sig_matrix.at['h3', col] = hf.at[index, 'h3']

    #print(database)
    #print(hf)
    return sig_matrix


def create_database(itemset):
    "Uses dummy indexing to create the binary database and then transpose it to get sets as columns"
    return pd.Series(itemset).str.join('|').str.get_dummies().T


def lsh_function(s_val, r_val, b_val):
    val = 1 - (1 - (s_val ** r_val)) ** b_val

    #return round(val, 7)
    return pd.DataFrame({"s": [s_val], "r": [r_val], "b": [b_val], "func_val": [val]}, columns=["s","r","b","func_val"])

if __name__ == '__main__':
    # Exercise 3.1.1
    list_1 = [1,2,3,4]
    list_2 = [2,3,5,7]
    list_3 = [2,4,6]

    print(f"Jaccard Similarity: {jaccard_similarity(list_1,list_2)}")
    print(f"Jaccard Similarity: {jaccard_similarity(list_1, list_3)}")
    print(f"Jaccard Similarity: {jaccard_similarity(list_2, list_3)}")

    # Exercise 3.2.2
    sentence = "The most effective way to represent documents as sets, for the purpose of identifying lexically" \
               " similar documents is to construct from the document the set of  short strings that appear within it."

    # Call function to generate stop words list
    stop_words = gen_stop_words(sentence, 3)

    # Shingle size: stop word + 2 following words
    shingle_size = 3

    # Print my shingles from sentence
    print(f"Shingles in sentence: {get_shingles(sentence, stop_words, shingle_size)}")

    # Exercise 3.3.3
    # Use professors code to turn itemsets into a binary database, with some added code to transpose the results
    dict_itemset = create_dict_from_file('minhash.txt')
    database = create_database(dict_itemset)
    signatures = compute_minhash_sigs(database)
    print(database)
    print(f"Minhash Signature Matrix:\n"
          f"{signatures}")

    # Binary nature screws it up... so let's use indexes where it is true!
    print(f"Jaccard Similarity [db vs signatures for series 0 & 1]: {jaccard_similarity(database[database[0]==1].index.tolist(), database[database[1]==1].index.tolist())} - {jaccard_similarity(signatures[0], signatures[1])}")
    print(f"Jaccard Similarity [db vs signatures for series 1 & 2]: {jaccard_similarity(database[database[0]==1].index.tolist(), database[database[3]==1].index.tolist())} - {jaccard_similarity(signatures[0], signatures[3])}")
    print(f"Jaccard Similarity [db vs signatures for series 2 & 3]: {jaccard_similarity(database[database[2]==1].index.tolist(), database[database[3]==1].index.tolist())} - {jaccard_similarity(signatures[2], signatures[3])}")

    # Exercise 3.4.1
    # create dict of r/b values
    rb_dict = {3: 10, 6: 20, 5: 50}

    # create a list of s values to loop over
    s_list = [.1, .2, .3, .4, .5, .6, .7, .8, .9]

    # create empty df with column names
    df_cols = ["s", "r", "b", "func_val"]
    s_curve_df = pd.DataFrame(columns=df_cols)

    for s in s_list:
        for k, v in rb_dict.items():
            the_return = lsh_function(s, k, v)
            s_curve_df = s_curve_df.append(the_return, ignore_index=True)

        #s_curve_df = s_curve_df.append(pd.Series(the_return, index=df_cols), ignore_index=True)
        #s_curve_df = s_curve_df.append(the_return)

    print(s_curve_df)

    fix, ax = plt.subplots()
    for key, grp in s_curve_df.groupby(['r','b']):
        ax = grp.plot(ax=ax, kind="line", x="s", y="func_val", label=f"r,b Value {key}")

    plt.legend(loc="best")
    plt.show()
