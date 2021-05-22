lst = [50, "Python", "JournalDev", 100]
print(list(zip(list(iter(lst))*2)))
lst_tuple = [x for x in zip(*[iter(lst)]*2)]
print(lst_tuple)
