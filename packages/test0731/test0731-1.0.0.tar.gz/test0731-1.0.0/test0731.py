'''
movies = [ "The Holy Grail",1975,"The Life of Brian",91,"The Meaning of Life",
           ["Graham Chapman",["Micheal Palin","John Cleese","Terry Gilliam",
                              "Eric Idle","Terry Jones"]]]
for each_flick in movies:
    if isinstance(each_flick,list):
        for each_flick1 in each_flick:
            if isinstance(each_flick1,list):
                for each_flick2 in each_flick1:
                    print(each_flick2)
            else:
                print(each_flick1)
    else:

        print(each_flick)#打开内嵌列表中的第一个内嵌列表，并直接用print读取列表数据      


'''

#定义函数，调用递归，直接解决上面的嵌套麻烦问题.注释的方法及格式
'''模块注释:这是"test_0731.py"模块，提供了一个名为print_lol()的函数，这个函数的作用是打印列表
包括可能的嵌套列表'''
def print_lol(the_list):
    '''(函数后面的注释要TAB)函数注释：这个函数取一个位置函数，名为"the_list"，
这可以是任何Python列表（可包含嵌套列表）。所指定的列表中的每个数据项会（递归地）
输出到屏幕上，各数据项各占一行。'''
    for each_item in the_list:
            if isinstance(each_item,list):
                #BIF—检查一个标识符是否指示某个指定类型的数据对象
                print_lol(each_item)
            else:
                print(each_item)
                
movies = [ "The Holy Grail",1975,"The Life of Brian",91,"The Meaning of Life",
           ["Graham Chapman",["Micheal Palin","John Cleese","Terry Gilliam",
                              "Eric Idle","Terry Jones"]]]

print_lol(movies)
######此处疑问：上面定义的函数可能会有重名问题，系统会自动分辨
#列表和标识符吗？（for 标识符 in 列表)



