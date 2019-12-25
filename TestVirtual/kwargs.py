import itertools


def myfunc(**kwargs):

    for key, value in kwargs.items():
        print(key + "; " + value)


myfunc(val = 'value1', name = 'larry', addr = 'mystreet')

a = 'a'
b = 'b'
print("a = %s  %s" % (a,b))

dic1 = {'v1': 1, 'v2': 2, 'v3': 3}
dic2 = {'z1': 1, 'z2': 2, 'z3': 3}

lst = [dic1,dic2]

print [e.keys() for e in lst]
ls = list(itertools.chain.from_iterable([e.keys() for e in lst]))
for e in ls:
    print e

print ls

a = range(1,10)
a = a + a
aa = reduce(lambda l, x: l + [x] if x not in l else l, lst,[])
pass
print aa

for p in ['Props', 'Property']:
    print p
