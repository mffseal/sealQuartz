---
title: spring
created: 2022-07-27 15:16:53
updated: 2022-09-18 22:17:02
tags: 
- atom
---

# spring

## 依赖注入

xml配置中常见形式 `<xxx name="abc", ref="abcBean">`：
1. setter注入时意味着：将前述创建的abcBean赋值给**成员**abc。
2. 构造器注入时意味着：将前述创建的abcBean传递给**形参**abc。 

> ref填的是前述定义的bean的id值。

> 构造器传递会受到构造函数形参的限制，造成配置文件与代码的耦合，虽然提供了部分兼容性的解决方案：指定参数类型、指定参数顺序，但还是不好用，自己开发模块推荐用setter。
