#a = {0: [1.2], 1: [4.3]}

#print(a.values())
#print(sum([sum(v) for v in a.values()]))
#print(sum(a.values()))

def elsweyr():
    return 1

d = {'a': elsweyr(), 'b': 2}

p = "->"

for k,v in d.items():
    print(k)
    print(v)
#    p += str(k) + ' -> ' + str(v)


#print(p)