def printmat(mat):
    if (len(mat) == 0):
        raise Exception('Matrix should be at least 1x1')
    x, y = len(mat[0]), len(mat)

    out = str(y) + ' ' + str(x) + '\n'
    out += '\n'.join([' '.join([str(c) for c in r]) for r in mat])

    return out
