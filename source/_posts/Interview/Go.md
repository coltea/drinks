---
title: Golang面试题
date: 2021-12-07 17:25:11
tags: 
 - Go
categories: 
 - Interview
---
# Go面试题

[TOC]

## 编程基础

#### nil

- 是变量名，而非关键字、保留字 可以覆盖（但不建议）
- 引用类型的零值


#### slice

当`slice`的容量小于1024时，容量是按照2倍大小增长的。当容量大于1024，增长的容量是原来的1.25倍



#### rune类型

中文长度判断 int32



#### 	new/make区别

```go
func new(Type) *Type
func make(t Type, size ...IntegerType) Type
```

- new：用于获取对应类型的指针类型,并进行内存分配置为零值
- make：引用类型的初始化(slice，map、chan) 返回传入的类型,用于引用类型的内存空间分配 



1. 入参不同: 

   make( )是slice，map、chan初始化 还可以加长度和容量

   new( )是struct 只接受一个参数

2. 返回

   new 返回值是一个指针，指向新分配的该类型的零值,

   make 直接返回的是Type类型值。

```go
	n1 := make([]A, 5)
	n2 := make([]*A, 5)
	n3 := new([]A)
	n4 := new([]*A)

	fmt.Println(n1, n1[0]) // [{ } { } { } { } { }] { }
	fmt.Println(n2, n1[0]) //  [<nil> <nil> <nil> <nil> <nil>] { }
	fmt.Println(n3)        //  &[]
	fmt.Println(n4)        //  &[]

	
```





#### 引用类型/值类型

- 值类型 int string float bool struct
- 引用类型 chanel slice map interface    可以用make初始化

引用类型需要分配内存空间



#### Go是值传递还是引用传递

全部是值传递，都是一个副本，一个拷贝。

但是因为拷贝的内容

有时候是非引用类型（int、string、struct等），这样就在函数中就无法修改原内容数据；

有的是引用类型（指针、map、slice、chan等），这样就可以修改原内容数据。




  #### 函数导入指针还是值

  	视情况而定 对原数据修改是指针，其他穿值

​	  （有外部调用会有逃逸 无关值类型还是指针类型）

#### json

数字默认解析为float64



#### 触发异常的场景

- 空指针解析
- 下标越界
- 除数为0
- 主线程阻塞 死锁 deadelock
- 解析错误 未加断言
- 调用 panic 函数



####  导包顺序/多个init能否执行

​	执行顺序是按照导入包的顺序执行，而不是按照调用先后顺序执行。

​	main开始 按顺序导包 import  然后按顺序执行init() 然后执行main函数代码



#### **多核CPU场景下，cache如何保持一致、不冲突？**

设置状态 



#### **uint类型溢出**

1-2 = 2^64 -1



#### defer 、painc的执行顺序

defer 的执行顺序是后进先出。当出现 panic 语句的时候，会先按照 defer 的后进先出的顺序执行，最后才会执行panic



#### **select可以用于什么？**

一个面向channel的 IO 监听操作,常用于gorotine的完美退出



#### 错误处理是怎么做的?





#### 数组扩容实现

append函数，因为slice底层数据结构是，由数组、len、cap组成，所以，在使用append扩容时，会查看数组后面有没有连续内存快，有就在后面添加，没有就重新生成一个大的数组。



#### golang中解析tag是怎么



#### 



## 编程进阶

#### 读一个空管道或写一个缓冲已经满的管道，到底会发生什么行为

1. 发生在非main协程里，则阻塞
2. 发生在main协程里
   2.1 没有其他非main协程可以执行，报 fatal error: all goroutines are asleep - deadlock!
    　　2.2 有其他非main协程可以执行，则main协程会让他们先执行
    　　　　2.2.1 非main协在程执行过程中，帮main协程解除了阻塞
    　　　　2.2.2 非main协执行结束后，依然没有帮main协程解除阻塞，则main协程报 fatal error: all goroutines are asleep - deadlock!



#### 实现的？反射原理是什么？通过反射调用函数‘



#### 子程 panic 为何没法被父协程 recover

 defer 在多个协程之间是没有效果，在子协程里触发 panic，只能触发自己协程内的 defer，而不能调用 main 协程里的 defer 函数的。



#### 性能优化

- 性能要求高（如用到cgo、文件） 可以加大p的数量runtime.GOMAXPROCS(GOMAXPROCS(0)+1)

- slice和map的容量初始化: 减少不断加元素时的扩容

- 减少反射 

  `reflect.Value` 会将对象拷贝并分配到堆上，程序中的对象都是消息体，有的消息体会超大，因此会分配较多的堆内存。

- GOGC=100调大（内存要足够大） 降低gc除非频率 

  golang 的 gc 时机是根据当前与上次的 heap size 的比例来决定

- 一点点拷贝胜过传指针: 对象在栈上分配, 减少GC频率.

- 全局缓存对象有大量的key的情况, value少用指针
  GC并发Mark需要mark存活的对象, 如果value里指针多, 导致mark消耗的CPU很大, 使用一个struct内嵌数据消除指针.



#### **pprof**

10ms/次收集

- CPU profile：报告程序的 CPU 使用情况，按照一定频率去采集应用程序在 CPU 和寄存器上面的数据
- Memory Profile（Heap Profile）：报告程序的内存使用情况
- Block Profiling：报告 goroutines 不在运行状态的情况，可以用来分析和查找死锁等性能瓶颈
- Goroutine Profiling：报告 goroutines 的使用情况，有哪些 goroutine，它们的调用关系是怎样的

runtime/pprof主要用于可结束的代码块，如一次编解码操作等；

net/http/pprof是对runtime/pprof的二次封装，主要用于不可结束的代码块，如web应用等。

- heap空间分析
- 函数执行时间
- svg的文件，用浏览器打开就是火焰图

#### trace

go tool trace，可以看到 p 绑定的 g 实际的 GC 动作和相应时长，以及阻塞时间



## Sync

#### WaitGroup

用于 多个 Goroutine  并发执行等待返回

```go
type WaitGroup struct {
	noCopy noCopy    //  保证 sync.WaitGroup 不会被开发者通过再赋值的方式拷贝；
	state1 [3]uint32  // 存储着状态和信号量；
}
```



#### 实现超时控制

- time,after
- context.WithTimeout()



 #### Mutex是悲观锁还是乐观锁？悲观锁、乐观锁是什么？

悲观锁

读写都是互斥

乐观锁本质不是锁 只是 

乐观锁实现 不能保证先进先出 没法做到线程安全



####  Mutex有几种模式？

- 正常模式

  1. 有抢占的机制 
  2. 被唤起的 Goroutine 与新创建的 Goroutine 竞争(被唤起的 Goroutine大概率会获取不到锁)

- 饥饿模式

  1. 新的 Goroutine 在该状态下不能获取锁、也不会进入自旋状态，它们只会在队列的末尾等待
  2. 严格的先来后到 全部都要排队  直接走队列先进先出 
  3. 饥饿模式的能避免 Goroutine 由于陷入等待无法获取锁而造成的高尾延时。



#### Mutex什么时候 进入/退出 饥饿模式？

> 进入饥饿模式

- 当队列头部超过1ms获取不到锁的时候

> 退出饥饿模式

- 队列为空

- 队列第一个锁获得时间小于1ms

  

#### Mutex可以做自旋锁吗？

 可以

#### 项目中用过的锁？



#### 信号量

信号量做并发量限制。



#### Go并发控制

- 全局共享变量加个互斥锁
- channel通信
- Context包





## Channel



#### **介绍一下channel**

缓冲

- 无缓存,同步,需要先有一个消费者 没有消费者先启动， 会导致死锁阻塞
- 有缓冲,异步 基于环形缓存的传统生产者消费者模型；

csp



在栈上的一个指向堆上的指针



#### **channel实现原理**

runtime库里的一个结构体，是一个用于同步和通信的有锁队列

```go
type hchan struct {
	qcount   uint  // Channel 中的元素个数；
	dataqsiz uint // Channel 中的循环队列的长度；
	buf      unsafe.Pointer  // Channel 的缓冲区数据指针；
  
	elemsize uint16   // Channel 能够收发的元素大小
	closed   uint32
	elemtype *_type  // Channel 能够收发的元素类型
  
	sendx    uint // Channel 的发送操作处理到的位置；
	recvx    uint  //Channel 的接收操作处理到的位置；
	recvq    waitq  // 接受等待队列
	sendq    waitq   // 发送等待队列

	lock mutex // 用于保护成员变量的互斥锁 mutex 来保证线程安全,使用互斥锁解决程序中可能存在的线程竞争问题,容易地实现有锁队列。  悲观互斥锁
}


type waitq struct {
	first *sudog
	last  *sudog
} // 表示一个在等待列表中的 Goroutine，该结构中存储了两个分别指向前后 runtime.sudog 的指针以构成链表。
```



- 用于保护成员变量的互斥锁 mutex 来保证线程安全,使用互斥锁解决程序中可能存在的线程竞争问题,容易地实现有锁队列。

- 有缓冲的数组 有字段来标记缓冲的队列长度

-  双指针 

- 环形队列

  

#### **channel是否线程安全？**

- 这个可以看源码就知道channel内部维护了一个互斥锁，来保证线程安全：
- 原子操作 
- CSP

 悲观互斥锁 只有一个goroutine 能拿到这个锁

#### **Channel分配在栈上还是堆上？**  

堆上







​     

## GMP

调度在计算机中是分配工作所需资源的方法. linux的调度为CPU找到可运行的线程. 而Go的调度是为M(线程)找到P(内存, 执行票据)和可运行的G.

#### 介绍一下GMP

**G:Goroutine**(用户态轻量线程)

- 
- 栈初始2KB, 调度不涉及系统调用.
- 用户函数调用前会检查栈空间是否足够, 不够的话, 会进行栈扩容

P:Processor(中间逻辑处理调度器)

- 

M:Machine Tread（操作系统分配到go的内核线程数）

- p的本地队列为空为自旋线程（过度状态 很快从全局或者work stealing 拿g）
- 

#### GMP线程模型

- 1:1  协程的创建、删除和切换的都由CPU完成，CPU开销过高

- 1:M  无法利用多核、线程阻塞会导致所有协程阻塞

- M:N  实现复杂

#### GMP流程

- 初始化 创建G0
- 创建goroutine
- 放入队列
  - 优先本地队列
  - 本地满了放全局队列
- M通过P获取G
  - 1/62 全局
  - 本地队列
  - 全局队列
  - 偷其他队列
- 4.执行

### goroutine

#### 介绍一下goroutine

- **内存消耗更少：**

Goroutine所需要的内存通常只有2kb，而线程则需要1Mb（500倍）。最大1GB

- **创建与销毁的开销更小**

由于线程创建时需要向操作系统申请资源，并且在销毁时将资源归还，因此它的创建和销毁的开销比较大。相比之下，goroutine的创建和销毁是由go语言在运行时自己管理的，因此开销更低。

- **切换开销更小**

这是goroutine于线程的主要区别，也是golang能够实现高并发的主要原因。线程的调度方式是抢占式的，如果一个线程的执行时间超过了分配给它的时间片，就会被其它可执行的线程抢占。在线程切换的过程中需要保存/恢复所有的寄存器信息，比如16个通用寄存器，PC（Program Counter），SP（Stack Pointer），段寄存器等等。

而goroutine的调度是协同式的，它不会直接地与操作系统内核打交道。当goroutine进行切换的时候，之后很少量的寄存器需要保存和恢复（PC和SP）。因此gouroutine的切换效率更高。

#### G0/M0的用途

G0

- M启动后创建的第一个G就是G0，每个M都会有一个自己的G0

- 仅用于负责调度，G0不指向任何可执行的函数。

- 在调度或系统调用时会使用G0的栈空间, 全局变量的G0是M0的G0。

M0

- 主线程，实例 runtime.m0

- 执行初始化操作和启动第一个G（即G0）， 在之后M0就和其他的M一致。

####  Goroutine调度顺序

- 放

  优先放本地队列 —> 满了 —> 全局队列

- 取

  1. 第一步，从全局运行队列中寻找goroutine。

     为了保证调度的公平性，每个工作线程每经过61次调度就需要优先尝试从全局运行队列中找出一个goroutine来运行，这样才能保证位于全局运行队列中的goroutine得到调度的机会。全局运行队列是所有工作线程都可以访问的，所以在访问它之前需要加锁。

  2. 第二步，从工作线程本地运行队列中寻找goroutine。

     如果不需要或不能从全局运行队列中获取到goroutine则从本地运行队列中获取。

  3. 第三步，从全局运行队列中寻找goroutine。

  4. 第四步，从其它工作线程的运行队列中偷取goroutine。

     如果上一步也没有找到需要运行的goroutine，则调用findrunnable从其他工作线程的运行队列中偷取goroutine，findrunnable函数在偷取之前会再次尝试从全局运行队列和当前线程的本地运行队列中查找需要运行的goroutine。



#### Goroutine的状态

![image-20211031142305144](https://tva1.sinaimg.cn/large/008i3skNly1gvyh2um0axj30t108lq4a.jpg)

#### Goroutine自旋占用cpu如何解决（go调用、gmp）

 



#### Goroutine抢占时机（gc 栈扫描）

STW的时候



####  goroutine什么时候会发生阻塞?

1. 由于原子、互斥量或通道操作调用导致  Goroutine  阻塞，调度器将把当前阻塞的 Goroutine 切换出去，重新调度 LRQ 上的其他 Goroutine；

2. 由于网络请求和 IO 操作导致  Goroutine  阻塞。

   Go 程序提供了网络轮询器（NetPoller）来处理网络请求和 IO 操作的问题，其后台通过 kqueue（MacOS），epoll（Linux）或  iocp（Windows）来实现 IO 多路复用。通过使用 NetPoller 进行网络系统调用，调度器可以防止  Goroutine  在进行这些系统调用时阻塞 M。这可以让 M 执行 P 的  LRQ  中其他的  Goroutines，而不需要创建新的 M。执行网络系统调用不需要额外的 M，网络轮询器使用系统线程，它时刻处理一个有效的事件循环，有助于减少操作系统上的调度负载。用户层眼中看到的 Goroutine 中的“block socket”，实现了 goroutine-per-connection 简单的网络编程模式。实际上是通过 Go runtime 中的 netpoller 通过 Non-block socket + I/O 多路复用机制“模拟”出来的。

3. 当调用一些系统方法的时候（如文件 I/O）

   ，如果系统方法调用的时候发生阻塞，这种情况下，网络轮询器（NetPoller）无法使用，而进行系统调用的  G1  将阻塞当前 M1。调度器引入 其它M 来服务 M1 的P。

4. 如果在 Goroutine 去执行一个 sleep 操作
   导致 M 被阻塞了。Go 程序后台有一个监控线程 sysmon，它监控那些长时间运行的 G 任务然后设置可以强占的标识符，别的 Goroutine 就可以抢先进来执行。





Go 中的阻塞分析有助于您分析程序在等待下列阻塞操作上的花费时间：

- select
- chan send
- chan receive
- semacquire ( `Mutex.Lock`, `RWMutex.RLock` , `RWMutex.Lock`, `WaitGroup.Wait`)
- notifyListWait ( `Cond.Wait`) 只有当 Go 通过将 goroutine 置于等待状态来暂停执行时，时间才会被跟踪。例如 `Mutex.Lock()`，如果锁可以立即或通过少量自旋被获得，那么这样的操作将不会出现在您的分析结果中。

上面的操作是 Go 运行时使用的等待状态的子集，下面的操作将不会出现在分析文件中：

- time.Sleep（但是 time.After, time.Tick 和其他封装了 channel 的操作会显示出来）
- 垃圾回收
- 系统调用（例如网络 I/O，文件 I/O 等）
- 运行时内部锁（例如 stopTheWorld）
- cgo 阻塞调用
- 永远阻塞的事件（例如在 nil 通道上发送/接收）
- 阻止尚未完成的事件

在某些场景下， Goroutine Profiling (debug=2) 可能是阻塞分析的一个很好的文档，因为它涵盖了所有等待状态，并且可以显示尚未完成且正在进行的阻塞事件。







#### goroutine阻塞了怎么办

- 原子、互斥量或通道、网络请求和 IO 操作、sleep

  调度器将把当前阻塞的 Goroutine 切换出去，重新调度 LRQ 上的其他 Goroutine

- 当调用一些系统方法的时候 syscall（如文件 I/O），

  而进行系统调用的 G将阻塞当前 M。调度器引入 其它M 来服务 M1 的P。

- sleep

  Go 程序后台有一个监控线程 sysmon，它监控那些长时间运行的 G 任务然后设置可以强占的标识符，别的 Goroutine 就可以抢先进来执行。





#### goroutine抢占的还是协作的 怎么实现

抢占

sysmon

当一个协程运行超过 10ms 时，Go 会尝试抢占它。10-20ms



#### 线程协程映射关系/线程模型

- **1:N:**  无法利用多核、线程阻塞会导致所以协程阻塞
- **1:1:**  协程的创建、删除和切换的都由CPU完成，CPU开销过高、
- **M:N:** 好用但是实现复杂



### Processor

​	上下文的逻辑处理调度器 

​    每个p有一个自己的本地goroutine队列

1. 复用线程

2. 避免频繁销毁创建，提高复用率
   - work stealing机制
   - 当本线程无可运行的G时，尝试从其他线程绑定的P偷取G。

   - hand off机制
   - 当本线程因为G进行系统调用阻塞时，线程释放绑定的P，把P转移给其他空闲的线程执行。

3. 利用并行

4. GOMAXPROCS利用多核CPU

   - GOMAXPROCS利用多核CPU

5. 抢占策略

   - goroutine最多占用CPU 10ms，

   - coroutine要等待协程主动释放

6. 全局队列

   - work stealing从其他P偷不到G时，它可以从全局G队列获取

## GC



#### Gc的类型

- 引用计数：对每个对象维护一个引用计数，当引用该对象的对象被销毁时，引用计数减1，当引用计数器为0是回收该对象。

  - 优点：对象可以很快的被回收，不会出现内存耗尽或达到某个阀值时才回收。
  - 缺点：不能很好的处理循环引用，而且实时维护引用计数，有也一定的代价。
  - 代表语言：Python、PHP、Swift

- 标记-清除：从根变量开始遍历所有引用的对象，引用的对象标记为"被引用"，没有被标记的进行回收。

  - 优点：解决了引用计数的缺点。
  - 缺点：需要STW，即要暂时停掉程序运行。
  - 代表语言：Golang(其采用三色标记法)




#### 介绍一下三色标记法

减少了STW的时间，即时标记，与程序并发执行

**流程**

- 所有对象最开始都是白色.

- 从root对象(栈对象和全局变量)开始找到可达对象，标记为灰色，放入待处理队列。

- 遍历灰色对象队列，将其引用对象标记为灰色放入待处理队列，自身标记为黑色。

- 循环步骤3直到灰色队列为空为止，

- 结束时所有引用对象都被标记为黑色，所有不可达对象为白色，

- 对剩下的白色进行回收

  

#### 介绍一下混合写屏障

为了解决误清扫

​	黑色对象创建新对象会变成白色，而黑色不是灰色一样会被扫描到

- 原理

  - 强三色不变式 黑色不允许引用白色
  - 弱三色不变式 黑色引用白色时白色上层需要有灰色

- 屏障机制

  - 插入屏障 黑色下游必须为灰色
  - 删除屏障

  

- 并发标记和清扫 内存耗尽，挂起程序，清扫所有未被引用的对象

 - 非分代和非紧缩

 Golang中的混合写屏障满足`弱三色不变式`，结合了删除写屏障和插入写屏障的优点，只需要在开始时并发扫描各个goroutine的栈，使其变黑并一直保持，



#### Gc触发时机

- **gcTriggerAlways**（废弃）：强制触发GC

- **gcTriggerHeap**：当前分配的内存达到一定阈值时触发，这个阈值在每次GC过后都会根据堆内存的增长情况和CPU占用率来调整

- **gcTriggerTime**：当一定时间没有执行过GC就触发GC（2分钟）

- **gcTriggerCycle**：调用runtime.GC()



#### Go内存管理方式

  

#### Go哪些对象分配在堆上，哪些对象分配在栈上？

逃逸分析(escape analysis)，当发现变量的作用域没有跑出函数范围**，**就可以在栈上**，**反之则必须分配在堆。

- 栈上-局部变量

- 堆上-全局、大内存变量

  

#### 介绍一下大对象小对象**，为什么小对象多了会造成gc压力？**

​	通常小对象过多会导致GC三色法消耗过多的GPU。优化思路是，减少对象分配



## 内存



类似于TCMalloc的结构  最小8B 最大 32KB

### 局部对象是分配到栈上还是分配到堆上，返回一个引用安全吗

Golang 中的变量只要被引用就会一直存活，Golang 编译器会将函数的局部变量分配到栈帧上，如果编译器不能确保变量return 后不再被引用，那么编译器会将它分配到堆上。**所以这里返回一个引用是安全的。** 并且如果局部变量非常大，那么它需要被分配在堆上而不是栈上。 并且Go 分成了微对象(0，16B)、小对象(16B,32KB)、大对象(32KB ,+∞)，微对象通过微分配器提高分配的性能，大对象会分配到栈上。



#### 内存分区

- arena

  堆区，go runtime 在动态分配的内存都在这个区域，并且将内存块分成 8kb 的页，一些组合起来的称为 

- bitmap

  用来标记堆区使用的映射表，它记录了哪些区域保存了对象，对象是否包含指针，以及 GC 的标记信息.

- spans

  存放 mspan 的指针，根据 spans 区域的信息可以很容易找到 mspan. 它可以在 GC 时更快速的找到的大块的内存 mspan.


#### 堆栈分别存储什么？

- 栈

- 编译器管理

  - 一级缓存

  - 自动申请、分配、释放。一般不会太大，我们常见的函数参数（不同平台允许存放的数量不同），局部变量等等都会存放在栈上

  - 函数调用的局部对象、变量

- 堆

  人为管理

  - 二级缓存

  - 手动申请、分配、释放。一般所涉及的内存大小并不定，一般会存放较大的对象。另外其分配相对慢，涉及到的指令动作也相对多，GC会回收，引用类型一般都分配到堆上。

  - 全局的对象、channel、需要共享的数据、超出分配的内存空间


#### 内存逃逸

编译时确定对象被分配到堆上还是栈上，这个步骤叫逃逸分析

- golang程序变量会携带有一组校验数据，用来证明它的整个生命周期是否在运行时完全可知。如果变量通过了这些校验，它就可以在栈上分配。否则就说它 逃逸 了，必须在堆上分配。

- 确认逃逸在编译阶段 确认变量的存放位置（堆还是栈）, 尽量放在栈上

- 全部在堆上

- 垃圾回收（GC）的压力不断增大
  - 申请、分配、回收内存的系统开销增大（相对于栈）
  - 动态分配产生一定量的内存碎片



#### OOM内存溢出

  pprof，拿到内存分布图

  gc在标记清除后，不会立马把空闲的内存还给系统，而是等待5分钟后的scvg来释放内存。

-   慢增型 http、db、长连接 close

-   突增型 内存泄露或新增大量内存占用的逻辑(例：过长的字符串) 

    go无法分配内存时 throw输出的协程栈pprof调试 结合火焰图, 查看影响性能的热点部分

火焰图

- 调用栈,长度代表cpu时长。


## 其他

#### 如何实现 deepcopy

- 深度拷贝可以通过序列化和反序列化来实现，

  `val := reflect.ValueOf(v)` 拿到 `v` 的反射值

- 也可以基于`reflect`包的反射机制完成。

[reflect.DeepEqual](https://link.zhihu.com/?target=https%3A//pkg.go.dev/reflect%3Ftab%3Ddoc%23DeepEqual) 检查

​	



