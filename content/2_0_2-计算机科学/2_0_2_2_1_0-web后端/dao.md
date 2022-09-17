---
title: dao
created: 2022-08-12 20:55:15
updated: 2022-08-12 20:57:50
tags: 
- atom
---
# dao

DAO（Data Access Object）是**用于访问数据的对象**，实际上是一个映射关系，将java中访问对象的操作映射的具体数据库的操作，例如Mybatis的设计中，MapperScannerConfigurer会扫描所有dao，得到domain数据对象操作和数据库语句的映射关系，通过[[2_0_2-计算机科学/2_0_2_1_2_0-软件语言/2_0_2_1_2_0_0-Java/2_0_2_1_2_0_0_1-高级特性/动态代理|动态代理]]的方式拦截所有对domain的操作，转到对数据库的操作。