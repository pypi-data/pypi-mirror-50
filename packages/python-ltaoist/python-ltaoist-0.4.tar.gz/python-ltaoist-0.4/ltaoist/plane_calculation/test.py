from PlaneSet import original, derive, query

@original('a')
def _():
    return []

@derive('b', ['a'])
def _(a):
    print(a)
    return a

query('b')
