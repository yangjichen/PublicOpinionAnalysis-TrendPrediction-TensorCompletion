"""This file contains some useful tools for tensor operation (some are integrated from pytensor packages)"""

import numpy as np
import cmath
import math


def uniquerows(arg):
    # made by GHC
    return np.unique(arg.view(np.dtype((np.void,
                                        arg.dtype.itemsize * arg.shape[1])))).view(arg.dtype).reshape(-1, arg.shape[1])


def prod(arg):
    """ returns the product of elements in arg.
    arg can be list, tuple, set, and array with numerical values. """
    ret = 1
    for i in range(0, len(arg)):
        ret = ret * arg[i]
    return ret


def allIndices(dim):
    """ From the given shape of dimenions (e.g. (2,3,4)),
    generate a numpy.array of all, sorted indices."""
    length = len(dim)
    sub = np.arange(dim[length - 1]).reshape(dim[length - 1], 1)
    for d in range(length - 2, -1, -1):
        for i in range(0, dim[d]):
            temp = np.ndarray([len(sub), 1])
            temp.fill(i)
            temp = np.concatenate((temp, sub), axis=1)
            if i == 0:
                newsub = temp
            else:
                newsub = np.concatenate((newsub, temp), axis=0)
        sub = newsub
    return sub


def find(nda, obj):
    """returns the index of the obj in the given nda(ndarray, list, or tuple)"""
    for i in range(0, len(nda)):
        if nda[i] == obj:
            return i
    return -1


def notin(n, vector):
    """returns a numpy.array object that contains
    elements in [0,1, ... n-1] but not in vector."""
    ret = np.arange(n).tolist()
    for i in vector:
        if 0 <= i < n:
            ret.remove(i)
    return np.array(ret)


def getelts(nda, indices):
    """From the given nda(ndarray, list, or tuple), returns the list located at the given indices"""
    ret = []
    for i in indices:
        ret.extend([nda[i]])
    return np.array(ret)


def sub2ind(my_shape, my_subs):
    """ From the given shape, returns the index of the given subscript"""
    revshp = list(my_shape)
    revshp.reverse()
    mult = [1]
    for i in range(0, len(revshp) - 1):
        mult.extend([mult[i] * revshp[i]])
    mult.reverse()
    mult = np.array(mult).reshape(len(mult), 1)

    print my_subs
    print mult


    idx = np.dot(my_subs, mult)
    return idx


def ind2sub(my_shape, ind):
    """ From the given shape, returns the subscrips of the given index"""
    revshp = []
    revshp.extend(my_shape)
    revshp.reverse()
    mult = [1]
    for i in range(0, len(revshp) - 1):
        mult.extend([mult[i] * revshp[i]])
    mult.reverse()
    mult = np.array(mult).reshape(len(mult))

    sub = []

    for i in range(0, len(my_shape)):
        sub.extend([math.floor(ind / mult[i])])
        ind = ind - (math.floor(ind / mult[i]) * mult[i])
    return sub


def tt_dimscehck(dims, n, m=None, exceptdims=False):
    """
    Checks whether the specified dimensions are valid in a Tensor of n-dimension.
    If m is given, then it will also retuns an index for m multiplicands.
    If exceptdims == True, then it will compute for the dimensions not specified.
    """

    # if exceptdims is true
    if exceptdims:
        dims = listdiff(range(0, n), dims)

    # check vals in between 0 and n-1
    for i in range(0, len(dims)):
        if dims[i] < 0 or dims[i] >= n:
            raise ValueError("invalid dimensions specified")

    # number of dimensions in dims
    p = len(dims)

    sdims = []
    sdims.extend(dims)
    sdims.sort()

    # indices of the elements in the sorted array
    sidx = []
    # table that denotes whether the index is used
    table = np.ndarray([len(sdims)])
    table.fill(0)

    for i in range(0, len(sdims)):
        for j in range(0, len(dims)):
            if sdims[i] == dims[j] and table[j] == 0:
                sidx.extend([j])
                table[j] = 1
                break

    if m is None:
        return sdims

    if m > n:
        raise ValueError("Cannot have more multiplicands than dimensions")

    if m != n and m != p:
        raise ValueError("invalid number of multiplicands")

    if m == p:
        vidx = sidx
    else:
        vidx = sdims

    return sdims, vidx


def listtimes(my_list, c):
    """multiplies the elements in the list by the given scalar value c"""
    ret = []
    for i in range(0, len(my_list)):
        ret.extend([my_list[i]] * c)
    return ret


def listdiff(list1, list2):
    """returns the list of elements that are in list 1 but not in list2"""
    if list1.__class__ == np.ndarray:
        list1 = list1.tolist()
    if list2.__class__ == np.ndarray:
        list2 = list2.tolist()
    ret = []
    for i in range(0, len(list1)):
        ok = True
        for j in range(0, len(list2)):
            if list[i] == list[j]:
                ok = False
                break
        if ok:
            ret.extend([list[i]])
    return ret


def tt_subscheck(my_subs):
    """Check whether the given list of subscripts are valid. Used for Sptensor"""
    isOk = True
    if my_subs.size == 0:
        isOk = True

    elif my_subs.ndim != 2:
        isOk = False

    else:
        for i in range(0, (my_subs.size / my_subs[0].size)):
            for j in range(0, my_subs[0].size):
                val = my_subs[i][j]
                if cmath.isnan(val) or cmath.isinf(val) or val < 0 or val != round(val):
                    isOk = False

    if not isOk:
        raise ValueError("Subscripts must be a matrix of non-negative integers")

    return isOk


def tt_valscheck(vals):
    """Check whether the given list of values are valid. Used for Sptensor"""
    isOk = True

    if vals.size == 0:
        isOk = True

    elif vals.ndim != 2 or vals[0].size != 1:
        isOk = False

    if not isOk:
        raise ValueError("values must be a column array")

    return isOk


def tt_sizecheck(size):
    """Check whether the given size is valid. Used for Sptensor"""
    size = np.array(size)
    isOk = True

    if size.ndim != 1:
        isOk = False
    else:
        for i in range(0, len(size)):
            val = size[i]
            if cmath.isnan(val) or cmath.isinf(val) or val <= 0 or val != round(val):
                isOk = False

    if not isOk:
        raise ValueError("size must be a row vector of real positive integers")
    return isOk


if __name__ == '__main__':
    shape = (4, 4, 4)
    subs = [0, 0, 0]
    print sub2ind(shape, subs)
