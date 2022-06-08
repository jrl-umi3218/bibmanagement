def distance(word1, word2):
    '''
    Compute the Levenshtein distance between 2 words, i.e. the minimum number
    of letter insertion, deletion or replacement needed to go from one word to
    the other
    '''
    n1 = len(word1)
    n2 = len(word2)
    row = [i for i in range(n2 + 1)]
    
    for w1 in range(1, n1 + 1):
        e = w1
        for w2 in range(1, n2 + 1):
            if (word1[w1-1] == word2[w2-1]):
                tmp = row[w2-1]
                row[w2-1] = e
                e = tmp
            else:
                l = [e, row[w2], row[w2-1]]
                row[w2-1] = e
                e = min(l) + 1
        row[n2] = e
            
    return row[n2]