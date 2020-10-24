#The basic outline of this problem is to read the file, look for integers using the re.findall(), looking for a regular expression of '[0-9]+' and then converting the extracted strings to integers and summing up the integers.

import re
fname = input("Enter file name: ")
fh = open(fname)
x= list()
for line in fh:
    y= re.findall('[0-9]+',line)
    x= x+y

sum= 0
for z in x:
    sum= sum + int(z)

print(sum)
