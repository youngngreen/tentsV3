# gives all combinations of the given list and length
from itertools import combinations, product, chain
def iterlist(lst, num):
    combs = combinations(lst, num)
    return [list(i) for i in combs]