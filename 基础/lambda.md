## lambda表达式
lambda表达式，通常是在**需要一个函数，但是又不想费神去命名一个函数** 的场合下使用，也就是指**匿名函数** 。   
lambda所表示的匿名函数的内容应该是很简单的，如果复杂的话，干脆就重新定义一个函数了。   
**Python的lambda表达式基本语法是在冒号（：）左边放原函数的参数，可以有多个参数，用逗号（，）隔开即可；冒号右边是返回值。**   
如：  lambda x,y : (x + y) 

1. 应用在函数式编程中  
Python提供了很多函数式编程的特性，如：map、reduce、filter、sorted等这些函数都支持函数作为参数，lambda函数就可以应用在函数式编程中。如下：   
将列表中的元素按照绝对值大小进行升序排列    
```
list1 = [3,5,-4,-1,0,-2,-6]
sorted(list1, key=lambda x: abs(x))
```

2. 应用在闭包中
```
def get_y(a,b):
     return lambda x:a*x+b
y1 = get_y(1,1)
y1(1) # 结果为2
>>> def get_y(a,b):
...   return lambda x:a*x+b
...
>>> y1=get_y(1,1)
>>>y1(1)
2
>>> y1(2)
3
>>> y1(3)
4
>>> y2=get_y(2,3)
>>> y2(1)
5
>>> y2(2)
7
>>> y2(3)
9
```
