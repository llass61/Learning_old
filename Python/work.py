import os

# A0 = dict(zip(('a','b','c','d','e'),(1,2,3,4,5)))
# print (A0)

arr1 = (1,2,3,4,5,6,7)
arr2 = (1,3,5,7)
out = [i for i in arr1 if not i in arr2]
print(out)

os.listdir(r'C:\users\llassetter')