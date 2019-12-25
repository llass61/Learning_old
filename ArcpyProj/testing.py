
# import sys
# sys.path.insert(0, r'C:\Users\llassetter\Grid-I\gridsight')
# import gdbTools
#
#
# myGDB = 'C:\Users\llassetter\Grid-I\epedev005-ll.sde'
# ret = arcpy.env.workspace = myGDB
#
#
#
# gdbTools.addLineFields(myGDB)

class Cust():
    vvar = 'vvv'

    def __init__(self):
        self.var1 = 'aaa'

    def myFunc(self):
        print ("in myFunc")
        return [1,2,3,4,5]

    def wrapper1(self): self.myFunc()
    def wrapper2(self): return self.myFunc()



myCust = Cust()

def doIt():
    print ("doIt")

for a, b, c in [
    ('a', doIt, 'c')]:
    print (a)
    print (c)
    print ("executing b")
    b()

mylist = { 'one': 1, 'two': 2 }
print dir(myCust)
print getattr(myCust, 'var1')

print ("start myFunc testing")
print (myCust.wrapper1())
print (myCust.wrapper2())

print ("\ntesting maps")
lst = ['a','b','c']
a = map(lambda x: ','.join(x), [lst, lst])
print (a)