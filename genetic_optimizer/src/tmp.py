a = {0: [1.2], 1: [4.3]}

print(a.values())
print(sum([sum(v) for v in a.values()]))
#print(sum(a.values()))