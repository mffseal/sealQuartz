---
title: Callable
created: 2022-05-26 09:58:45
updated: 2022-05-26 10:21:43
tags: 
- atom
---
# Callable

带返回值的call，并且可以抛出异常。

```java
public interface Callable<V> {  
    V call() throws Exception;
```

