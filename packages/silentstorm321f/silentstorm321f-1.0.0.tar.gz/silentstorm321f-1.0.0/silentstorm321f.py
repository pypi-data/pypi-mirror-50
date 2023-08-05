print("hello world!")
wife = 'gaojie'
husband = 'zhangyu'
family = [wife,husband]
family.append('gaogao')
print(family)

movies = ['Shawshank\'s Rependition', 1994, ['Stephen King',['Tim Robbins','Morgan Freeman','Bob Gunton']]]
'''for i in movies:
    if isinstance(i,list):
        for j in i:
            print(' ',j)
    else:
        print(i)
'''
def print_list(the_list):
    for i in the_list:
        if isinstance(i,list):
            print(' ') 
            print_list(i)
        else:
            print(i)

print_list(movies)