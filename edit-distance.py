############
## https://github.com/kaldi-asr/kaldi/blob/6e03a3f5f99d6d8c22494d90b7e7f9ceb0117ac8/src/util/edit-distance-inl.h#L104
## KALDI SUBTITUTION COST is ONE

## OTHER REFERENCE https://web.stanford.edu/class/cs124/lec/med.pdf
## OTHER REFERENCE https://stackoverflow.com/questions/66636450/how-to-implement-alignment-through-traceback-for-levenshtein-edit-distance
############

import numpy as np

def word_edit_distance(x, y):
    rows = len(x) + 1
    cols = len(y) + 1
    distance = np.zeros((rows, cols), dtype=int)
    pointer = np.zeros((rows, cols), dtype=int)

    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k
            

    for col in range(1, cols):
        for row in range(1, rows):
            if x[row - 1] == y[col - 1]:
                cost = 0
            else:
                cost = 1

            distance[row][col] = min(distance[row - 1][col - 1] + cost,
                                     distance[row - 1][col] + 1,
                                     distance[row][col - 1] + 1)
            
            if distance[row][col] == distance[row - 1][col - 1] + cost:
                if cost == 0:
                    pointer[row][col] = 4
                elif cost == 1:
                    pointer[row][col] = 3
                
            elif distance[row][col] == distance[row - 1][col] + 1:
                pointer[row][col] = 2
            else:
                pointer[row][col] = 1
                
    row = rows - 1
    col = cols - 1
    
    hyp_ali = []
    ref_ali = []
    
#     print(row, col)
    while row != 0 and col != 0:
        
        if pointer[row][col] == 1:
            hyp_ali.append('***')
            ref_ali.append(y[col - 1])
            col -= 1
            
        elif pointer[row][col] == 2:
            hyp_ali.append(x[row - 1])
            ref_ali.append('***')
            row -= 1
            
        elif pointer[row][col] == 3:
            hyp_ali.append(x[row - 1])
            ref_ali.append(y[col - 1])
            col -= 1
            row -= 1
            
        elif pointer[row][col] == 4:
            hyp_ali.append(x[row - 1])
            ref_ali.append(y[col - 1])
            col -= 1
            row -= 1
            
#         print(row, col)
        
    if col == 0 and row != 0:
        for i in range(row):
            hyp_ali.append(x[row - i - 1])
            ref_ali.append('***')
    elif col != 0 and row == 0:
        for i in range(col):
            hyp_ali.append('***')
            ref_ali.append(y[col - i - 1])
    elif col == 0 and row == 0:
        pass    
        
    hyp_ali.reverse()
    ref_ali.reverse()

    edit_distance = distance[rows-1][cols-1]
    return edit_distance, distance, pointer, hyp_ali, ref_ali

ref = 'a b c d e f g'.split()
hyp = 'q w b c r e f g z'.split()
result = word_edit_distance(ref, hyp)
print(result[0])
print(result[1])
print(result[2])
print(result[3])
print(result[4])
