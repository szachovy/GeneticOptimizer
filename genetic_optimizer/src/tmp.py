#a = {0: [1.2], 1: [4.3]}

#print(a.values())
#print(sum([sum(v) for v in a.values()]))
#print(sum(a.values()))

d = {'a': 1, 'b': 2}

p = "->"

for k,v in enumerate(d):
    p += str(k) + ' -> ' + str(v)


print(p)