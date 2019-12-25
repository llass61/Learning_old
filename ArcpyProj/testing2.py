import arcpy


class Class1(object):

    def __init__(self,var1):
        self.mylist = ['a','b']
        self.var1 = var1

class OuterClass(object):
    myClass = Class1('inner')

lst = [Class1("var1"), Class1("var2")]

aaa = OuterClass()

a = lst[0]
#b = lst['Class1']
c = ('a', 'b')
print (lst)
pass

for fn in ['f%s%s_%s'%(t,i,p)  for t in ['i'] for p in ['a','b','c'] for i in ['r','i']]: # fault impedances (phase)
    print (fn);

# tools = arcpy.ListTools("*_analysis")
# for tool in tools:
#     print (arcpy.Usage(tool))

print help(arcpy.Clip_analysis)

print (arcpy.ListEnvironments())

print (arcpy.CheckProduct("arcinfo"))

arcpy.Exists()
