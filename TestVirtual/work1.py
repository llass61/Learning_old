
#testing getattr
class Class1():

    def __init__(_self):
        _self.var1 = 'var1'
        _self.var2 = 'var2'


cl = Class1()

print getattr(cl, 'var3', 'None')
print cl.var1

a = (1,2,3,4)
b = (5,6,7,8)
zipped = zip(a, b)
print (zipped)

print (dict(zipped))

v = a.index(4)
print v

