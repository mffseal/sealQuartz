---
title: 双层not_exists嵌套
created: 2022-09-17 22:03:17
updated: 2022-09-17 22:04:28
tags: 
- article
---
# 双层not_exists嵌套

> [SQL 中的 EXISTS 到底做了什么？ - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/20005249)
> [SQL 双层 not exist 嵌套](https://blog.csdn.net/mtawaken/article/details/6573122)  

## WHERE 做了什么

```sql
SELECT Sno, Sname
FROM Student
WHERE Sdept = 'IS'
```

1. DBMS 会扫描 表中的每一条记录
1. 判断后面的逻辑表达式的值是否为 True
   - 如果为 True，则将当前这条记录放到结果集里面去
   - 如果逻辑表达式的值为 False 则不放

## 相关子查询

查询每个学生超过其选修的所有课程的平均成绩的课程的课程号:   
```sql
SELECT Cno
FROM SC x
WHERE Grade >=
(
    SELECT AVG(Grade)
    FROM SC y
    WHERE y.Sno = x.Sno
)
```

1. 扫描父查询中数据来源（如 SC 表）中的每一条记录
1. 将当前这条记录中的，在子查询中会用到的值(Grade)代入到子查询中去
1. 执行子查询并得到结果（可以看成是返回值）
1. 再将这个结果代入到父查询的条件中(Grade >=)
1. 判断父查询的条件表达式的值是否为 True (WHERE 起作用)
   - 若为 True，则将当前 SC 表中的这条记录（经过 SELECT 处理）后放到结果集中去
   - 若为 False 则不放

## (NOT) EXISTS 做了什么

若存在:
1. 判断子查询得到的结果集是否是一个空集
   - 如果不是，则返回 True
   - 如果是，则返回 False
若不存在:
返回结果与上述相反

### 用法

- 由exists引出的子查询，其目标列表达式通常都用*，因为EXISTS的子查询只返回真值或者假值，不返回选择出来的结果
- 子查询中必须要有依赖父查询的条件
- 每次查询时父查询表中的一个元组对子查询所有的元组进行判定
  - 如果为true则父查询中的这个元组允许放入结果表
  - 否则进行父查询下一个元组的判定

## WHERE 和 (NOT) EXISTS 配合

1. WHERE 根据其后语句的结果决定是否将当前遍历条目加入到结果集合中
1. EXISTS 用于检验当前条目相关数据带入自身判断后的逻辑结果
   1. 返回的是内部查询结果集是否为空的逻辑值
1. WHERE 接受 EXISTS 返回的逻辑值做相应操作

## 关系模型

```
学生（学号，姓名，系别，年龄）

课程（课程号，课程名，学时）

选读（学号，课程号，成绩）
```

## 问题: 检索选读全部课程的学生姓名

答案:
```sql
select 学生.姓名 from 学生
where not exists
(
    select * from 课程 where not exists
    (
        select * from 选读 where 学号=学生.学号 and 课程号=课程.课程号
    )
)
```

## 分析

1. 先取 Student 表中的第一个元组，得到其 Sno 列的值。
1. 再取 Course 表中的第一个元组，得到其 Cno 列的值。
1. 根据 Sno 与 Cno 的值，遍历 SC 表中的所有记录（也就是选课记录）
   - 第二个 NOT EXISTS
   - 若对于某个 Sno 和 Cno 的值来说，在 SC 表中找不到相应的记录，则说明该 Sno 对应的学生没有选修该 Cno 对应的课程。
1. 对于某个学生来说，若在遍历 Course 表中所有记录（也就是所有课程）后，仍找不到任何一门他/她没有选修的课程，就说明此学生选修了全部的课程。
   - 第一个 NOT EXISTS
1. 将此学生放入结果元组集合中。
1. 回到 STEP1，取 Student 中的下一个元组。
1. 将所有结果元组集合显示。

第一个 NOT EXISTS 对应第四步，第二个 NOT EXISTS 对应第三步

注释:

```sql
select 学生.姓名 from 学生  --结果集1, 结果集2为空对应的学生放入结果集1
where not exists
(
    select * from 课程  --结果集2, 课表里x同学未选过的课组成
    where not exists
    (
        select * from 选读
        where 学号=学生.学号 and 课程号=课程.课程号  --找学生x选过的课的集合
    )
)
```