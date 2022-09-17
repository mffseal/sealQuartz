---
title: tomcat原理
created: 2022-08-15 20:51:13
updated: 2022-08-15 21:16:38
tags: 
- atom
---
# tomcat原理

![[z-oblib/z2-attachments/Pasted image 20220815211547.png]]

## 右边 -- 请求处理

![[z-oblib/z2-attachments/Pasted image 20220815210239.png]]

wrapper的作用是给具体的servlet实现进行分类，每个servlet实现对应一个wrapper，存储多个运行时产生的实例。

>作用的防止混乱。

valve本身是一个责任链的模式，例如可以自定义valve来记录日志。
请求到达对应层次的时候，tomcat就会将请求传递给valve链处理，最终从StandardEngineValve将请求转交给下一层。

Wrapper中最后一个valve（StandardWrapperValve）会调用具体的业务servlet实例对象上的方法，统一调用service方法（servlet父类方法）， service根据http头的动作字符串（GET/POST。。）调用对应的方法。


## 左边 -- 请求产生

