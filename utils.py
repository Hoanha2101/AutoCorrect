from library import *

def process_data(file_name):
    """
    Input: 
        A file_name which is found in your current directory. You just have to read it in. 
    Output: 
        words: a list containing all the words in the corpus (text file you read) in lower case. 
    """
    words = [] # return this variable correctly

    ### START CODE HERE ### 
    
    #Open the file, read its contents into a string variable
    
    # convert all letters to lower case
    
    with open(file_name) as f:
        text = f.read().lower()
    #Convert every word to lower case and return them in a list.
    words = re.findall(r'\w+', text)
    
    ### END CODE HERE ###
    
    return words


# word_l = process_data('./data/shakespeare.txt')
# vocab = set(word_l)
    
# with open("./data/word_l.pickle", "wb") as handle:
#     pickle.dump(word_l, handle)
    
# with open("./data/vocab.pickle", "wb") as handle:
#     pickle.dump(vocab, handle)


def get_count(word_l):
    '''
    Input:
        word_l: a set of words representing the corpus. 
    Output:
        word_count_dict: The wordcount dictionary where key is the word and value is its frequency.
    '''
    
    word_count_dict = {}  # fill this with word counts
    ### START CODE HERE 
    for word in word_l:
        word_count_dict[word] = word_count_dict.get(word,0)+1
            
    ### END CODE HERE ### 
    return word_count_dict

def get_probs(word_count_dict):
    '''
    Input:
        word_count_dict: The wordcount dictionary where key is the word and value is its frequency.
    Output:
        probs: A dictionary where keys are the words and the values are the probability that a word will occur. 
    '''
    probs = {}  # return this variable correctly
    
    ### START CODE HERE ###
    
    # get the total count of words for all words in the dictionary
    M = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key]/M
    ### END CODE HERE ###
    return probs

# with open("./data/word_l.pickle", 'rb') as handle:
#     word_l = pickle.load(handle)
# word_count_dict = get_count(word_l)
# probs = get_probs(word_count_dict)

# with open("./data/probs.pickle", "wb") as handle:
#     pickle.dump(probs, handle)

"""  String Manipulations """

def delete_letter(word, verbose=False):
    '''
    Input:
        word: the string/word for which you will generate all possible words 
                in the vocabulary which have 1 missing character
    Output:
        delete_l: a list of all possible strings obtained by deleting 1 character from word
    '''
    
    delete_l = []
    split_l = []
    
    ### START CODE HERE ###
    for i in range(len(word)):
        split_l.append((word[:i], word[i:]))
    
    for conc in split_l:
        delete_l.append(conc[0] + conc[1][1:])
    
    ### END CODE HERE ###

    if verbose: print(f"input word {word}, \nsplit_l = {split_l}, \ndelete_l = {delete_l}")

    return  delete_l

def switch_letter(word, verbose=False):
    '''
    Input:
        word: input string
     Output:
        switches: a list of all possible strings with one adjacent charater switched
    ''' 
    
    switch_l = []
    split_l = []
    
    ### START CODE HERE ###
    split_l = [(word[:i], word[i:]) for i in range(len(word))]
    switch_l = [L + R[1] + R[0] + R[2:] for L, R, in split_l if len(R) >= 2]
    
    ### END CODE HERE ###
    
    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nswitch_l = {switch_l}") 
    
    return switch_l

def replace_letter(word, verbose=False):
    '''
    Input:
        word: the input string/word 
    Output:
        replaces: a list of all possible strings where we replaced one letter from the original word. 
    ''' 
    
    letters = 'abcdefghijklmnopqrstuvwxyz'
    
    replace_l = []
    split_l = []
    
    ### START CODE HERE ###
    split_l = [(word[:i], word[i:]) for i in range(len(word))]
    replace_set = [L + c + R[1:] for L, R in split_l for c in letters if c != R[0]]
    
    ### END CODE HERE ###
    
    # turn the set back into a list and sort it, for easier viewing
    replace_l = sorted(list(replace_set))
    
    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nreplace_l {replace_l}")   
    
    return replace_l

def insert_letter(word, verbose=False):
    '''
    Input:
        word: the input string/word 
    Output:
        inserts: a set of all possible strings with one new letter inserted at every offset
    ''' 
    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_l = []
    split_l = []
    
    ### START CODE HERE ###
    split_l = [(word[:i], word[i:]) for i in range(len(word)+1)]
    insert_l = [L + c + R for L, R in split_l for c in letters]
        
    ### END CODE HERE ###
    
    if verbose: print(f"Input word {word} \nsplit_l = {split_l} \ninsert_l = {insert_l}")
    
    return insert_l

def edit_one_letter(word, allow_switches = True):
    """
    Input:
        word: the string/word for which we will generate all possible wordsthat are one edit away.
    Output:
        edit_one_set: a set of words with one possible edit. Please return a set. and not a list.
    """
    
    edit_one_set = set()
    
    ### START CODE HERE ###
    edit_one_set = set(insert_letter(word)+delete_letter(word)+replace_letter(word))
    if (allow_switches):
        edit_one_set = edit_one_set.union(set(switch_letter(word,verbose=False)))
    
    ### END CODE HERE ###
    
    # return this as a set and not a list
    return set(edit_one_set)

def edit_two_letters(word, allow_switches = True):
    '''
    Input:
        word: the input string/word 
    Output:
        edit_two_set: a set of strings with all possible two edits
    '''
    
    edit_two_set = set()
    
    ### START CODE HERE ###
    edit_one_set = edit_one_letter(word, allow_switches=allow_switches)
    edit_two_set = edit_one_set
    for w in edit_one_set:
        edit_two_set = edit_two_set.union(set(edit_one_letter(w,allow_switches=allow_switches)))
        
    ### END CODE HERE ###
    
    # return this as a set instead of a list
    return set(edit_two_set)

def get_corrections(word, probs, vocab, n=2):
    '''
    Input: 
        word: a user entered string to check for suggestions
        probs: a dictionary that maps each word to its probability in the corpus
        vocab: a set containing all the vocabulary
        n: number of possible word corrections you want returned in the dictionary
    Output: 
        n_best: a list of tuples with the most probable n corrected words and their probabilities.
    '''
    
    suggestions = []
    n_best = []
    
    ### START CODE HERE ###
    #Step 1: create suggestions as described above    
    temp = []
    if word in probs.keys():    
        temp+=[(word, probs[word])]
    temp+=sorted([(w, probs[w]) for w in edit_one_letter(word) if w in probs], key=lambda x: -x[1])
    # temp+=sorted([(w, probs[w]) for w in edit_two_letters(word) if w in probs], key=lambda x: -x[1])
    suggestions = set([sugg[0] for sugg in temp[:n]])
                    
    #Step 2: determine probability of suggestions
    
    #Step 3: Get all your best words and return the most probable top n_suggested words as n_best
    
    n_best = [sugg for sugg in temp[:n]]
    
    ### END CODE HERE ###
    

    return n_best
