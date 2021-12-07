---
title: MySQL
date: 2021-03-27 23:13:11
tags: 
 - Database
categories: 
 - Database
---
# MySQL



## SQL

```mysql
# 从不订购的客户
select a.Name as Customers  from Customers  a
left join Orders b on a.Id=b.CustomerId 
Where b.Id is null 

select a.Name as `Customers`  from Customers  a
where id not in (select distinct CustomerId from Orders)


# 总分前三的学生姓名
SELECT `name` from (
  SELECT b.`name`,SUM(a.score)
  from score a 
  join student b on a.student_id=b.id
  GROUP BY  b.`name`
  ORDER BY SUM(a.score) desc limit 3
) as t


# 每门课成绩前五名
SELECT a.class,a.`name`,a.score from grade a 
WHERE (SELECT COUNT(1) from grade b WHERE a.class=b.class and  a.score <b.score)<5
ORDER BY class,score desc


SELECT a.class,a.`name`,a.score ,COUNT(b.score) as "No"   from grade a 
left join  grade b on a.class=b.class and a.score< b.score
GROUP BY a.class,a.`name`,a.score
HAVING COUNT(b.score) <5
ORDER BY a.class,a.score desc



# 获取所有部门中当前员工薪水最高的相关信息
select r.dept_no,ss.emp_no,r.maxSalary from (
  select d.dept_no,max(s.salary)as maxSalary from dept_emp d,salaries s
  where d.emp_no=s.emp_no
  group by d.dept_no
)as r,salaries ss,dept_emp dd
where r.maxSalary=ss.salary and r.dept_no=dd.dept_no and dd.emp_no=ss.emp_no
order by r.dept_no asc




```



> #### **为什么用id做主键**？

1. 行内约定规范（例如阿里官方的java开发手册 id、create_time、update_time 是表的必备字段，其中id为主键）
2. 可以唯一标识一行，
3. 数据自增 id 是顺序的，可以保证索引树上的数据比较紧凑，有更高的空间利用率以及减少数据页的分裂合并等操作，提高效率。
4. 空间占用相对较少 整型做主键，则只要4个字节 利于回表：先在二级索引查询到对应的主键值，然后根据主键再去聚簇索引里面取查询。其他的唯一索引例如手机号、身份证号作为主键等可能比较长 32





### 事务

ACID（Atomicity、Consistency、Isolation、Durability，即原子性、一致性、隔离性、持久性）

脏读（dirty read）、不可重复读（non-repeatable read）、幻读（phantom read）

### 隔离级别

数据库事务transanction正确执行的四个基本要素。ACID,原子性(Atomicity)、一致性(Correspondence)、隔离性(Isolation)、持久性(Durability)。

- 原子性:整个事务中的所有操作，要么全部完成，要么全部不完成，不可能停滞在中间某个环节。事务在执行过程中发生错误，会被回滚（Rollback）到事务开始前的状态，就像这个事务从来没有执行过一样。

- 一致性:在事务开始之前和事务结束以后，数据库的完整性约束没有被破坏。

- 隔离性:隔离状态执行事务，使它们好像是系统在给定时间内执行的唯一操作。如果有两个事务，运行在相同的时间内，执行 相同的功能，事务的隔离性将确保每一事务在系统中认为只有该事务在使用系统。这种属性有时称为串行化，为了防止事务操作间的混淆，必须串行化或序列化请 求，使得在同一时间仅有一个请求用于同一数据。

- 持久性:在事务完成以后，该事务所对数据库所作的更改便持久的保存在数据库之中，并不会被回滚。

  

- 【**脏读**】读未提交是指，一个事务还没提交时，它做的变更就能被别的事务看到。

- 【**不可重复读**】读提交是指，一个事务提交之后，它做的变更才会被其他事务看到。

- 【幻读】可重复读是指，一个事务执行过程中看到的数据，总是跟这个事务在启动时看到的数据是一致的。当然在可重复读隔离级别下，未提交变更对其他事务也是不可见的。

- 可串行化，顾名思义是对于同一行记录，“写”会加“写锁”，“读”会加“读锁”。当出现读写锁冲突的时候，后访问的事务必须等前一个事务执行完成，才能继续执行。

  

不可重复读指的是数据修改、幻读指的是数据增加不涉及修改



### MVCC

就是多版本并发控制。MVCC 是一种并发控制的方法，一般在数据库管理系统中，实现对数据库的并发访问。

MVCC只在 READ COMMITTED 和 REPEATABLE READ 两个隔离级别下工作。