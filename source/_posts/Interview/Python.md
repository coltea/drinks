---
title: Python面试题
date: 2021-03-27 23:26:11
tags: 
 - Python
categories: 
 - Interview
---
# Python面试题

[TOC]

### 基础

#### args/kwargs

args 不定数量的输入参数

kwargs 不定数量的键值对输入参数

`*args`必须在`**kwargs`前面



#### 创建类 带上project



#### 生成器/迭代器

迭代器

记录计算方法 不实际存储列表数据到内存中，是一种延迟计算方法， range函数实现的就是一种迭代器

生成器

本质也是一种迭代器，yield语句

- 就是用于迭代操作（for 循环）的对象，何实现了 `__next__` 方法 
- 不需要像列表把所有元素一次性加载到内存，而是以一种延迟计算方式返回元素

生成器

- 函数加上 yiled参数 
- 生成器本质上也是一个迭代器
- 生成器表达式用（）

[Generator](https://docs.python.org/zh-cn/3/glossary.html#term-generator) 是一个用于创建迭代器的简单而强大的工具。 它们的写法类似标准的函数，但当它们要返回数据时会使用 [`yield`](https://docs.python.org/zh-cn/3/reference/simple_stmts.html#yield) 语句。类似 go里面channel通道接受io、

迭代器 节省内存, 每次生成一个元素, 而不是先计算出所有的元素, 保存下来.



#### 装饰器

解决重复性的操作，功能抽离

- 计算函数运行时间
- 给函数打日志
- 类型检查
- 打开db的连接



#### is和 == 的区别

is是比较对象的id，而==仅比较对象的值，



#### 数据结构

- dict-hashmap
- list-链表
- tuple-
- set



#### 魔法方法

- `__add__`

- `__dict__`

  



#### 下划线开头函数



`__init__ / __new__`

1. init是初始化方法 实例方法，new是构造方法 静态方法

2. new在init之前执行, 用于创建对象并返回对象（可返回实例如不可变对象）

3. init返回None、new返回对象或者实例

4. 绝大多数情况下，我们都不需要自己重写__new__方法，但在当继承一个不可变的类型（例如str类,int类等）时，则需要用到new。

    

`__getter__ / __setter__`





#### 编码区别

- ascii
- unicode
- Utf-8



#### 模块查找顺序

- 内置的模块（python解释器自带的）
- 第三方（开发者编写的模块）
- 自定义的模块（自己编写的模块）



#### with关键词

__ENTER

__END



### 进阶

##### 协程

- N:1，Python协程模式，多个协程在一个线程中切换。在IO密集时切换效率高，但没有用到多核
- 协程通信是并发 不会并行 因为在单线程内执行 所以线程安全不需要考虑互斥 
- 

#### 性能优化

- c扩展
- pypy
- profile查看性能热点
- 非cpu密集型用异步、多线程
- 火焰图
- profile_line
- 

#### 正则

- 贪婪与非贪婪

#### GC

- 循环应用导致引用计数无法清零、导致GC无法进行垃圾回收
- 函数默认参数使用引用类型(dict、list)

多线程

- async await

flask

- context



#### 存在GIL，为什么还要加现场锁

GIL的线程安全是针对他自身Cpython的接口、字节码是按顺序执行的 （比如GC的应用计数）

并非用户态的代码是线程安全的的

用户的线程是可以切换执行的








#### 进程/线程/协程

进程下的多个线程可以共享该进程的所有资源，进程之间相互独立

- **多进程**:cpu密集走进程,进程资源开销大，但相对稳定
- **多线程:**io 密集走线程,python 有gil多线程只能发挥单核的性能 

在CPU密集的程序中，线程有点鸡肋，无法发挥多处理器的效率，这一点可以用进程来做。

在IO 密集的程序中，大量时间都花在等待IO上，对CPU不敏感，线程可以很好的胜任。



### 编程题


#### 字典按key排序

```python
alist = [{'name':'a','age':20},{'name':'b','age':30},{'name':'c','age':25}] 

def sort_by_age(list1): 
  return sorted(alist,key=lambda x:x['age'],reverse=True)
```

 #### 装饰器实现单例





#### GC

Python内部使用引用计数，来保持追踪内存中的对象，所有对象都有引用计数。

引用计数增加的情况：

1，一个对象分配一个新名称

2，将其放入一个容器中（如列表、元组或字典）

引用计数减少的情况：

1，使用del语句对对象别名显示的销毁

2，引用超出作用域或被重新赋值



1，当一个对象的引用计数归零时，它将被垃圾收集机制处理掉。

2，当两个对象a和b相互引用时，del语句可以减少a和b的引用计数，并销毁用于引用底层对象的名称。然而由于每个对象都包含一个对其他对象的应用，因此引用计数不会归零，对象也不会销毁。（从而导致内存泄露）。为解决这一问题，解释器会定期执行一个循环检测器，搜索不可访问对象的循环并删除它们。

内存溢出问题

1. 对象一直被全局变量所引用, 全局变量生命周期长.

2. 垃圾回收机被禁用或者设置成debug状态, 垃圾回收的内存不会被释放.

    

#### 内存池机制

Python提供了对内存的垃圾收集机制，但是它将不用的内存放到内存池而不是返回给操作系统。

1，Pymalloc机制。为了加速Python的执行效率，Python引入了一个内存池机制，用于管理对小块内存的申请和释放。



#### 内置函数

 with `__enter__` 和 `__exit__` 方法




#### 元类

​	相当于类的父类 用于创建类。python所以的东西都是对象，都是从一个类里面创建出来的，type就是python的内建元类。

django 用元类实现插件化与语法糖

#### asyncio

​	异步非阻塞，内部可以await 停止做其他的操作比如网络

​	fastapi



#### 私有变量

- 约定俗成、不是强制







#### 装饰器

抽离出大量函数中与函数功能本身无关的雷同代码并继续重用

- 日志

- 资源开销型 with外写





### Flask

current_app 是应用上下文。应用程序运行过程中，保存的一些配置信息，

request、session 是请求上下文。保存了客户端和服务器交互的数据。





### 设计模式

#### 单例

- 装饰器

  ```python
  def singleton(cls): 
  	instances = {} 
  	def wrapper(*args, **kwargs): 
  			if cls not in instances: 
  				instances[cls] = cls(*args, **kwargs) 
          return instances[cls] 
      return wrapper 
  
  @singleton 
  class Foo(object): 
  	pass 
  	
  foo1 = Foo() 
  foo2 = Foo() 
  print(foo1 is foo2) # True
  ```

- 使用基类，重写`__new__`方法

- 使用元类，type + metaclass



#### 多重继承

搜索从父类所继承属性的操作是深度优先、从左至右、递归查找。 派生类方法覆盖重载基类





#### Classmethod / staticmethod

​		**相同**

- 都不需要实例化，即可调用

- 类方法需要cls参数传入，静态函数则不用

  **区别**

- 类函数可以当做作为类似`__new__`一样的构造函数，用来返回类对象

 