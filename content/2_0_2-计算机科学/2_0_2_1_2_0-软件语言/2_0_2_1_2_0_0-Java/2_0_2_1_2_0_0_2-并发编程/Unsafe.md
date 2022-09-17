---
title: Unsafe
created: 2022-06-04 22:42:50
updated: 2022-06-06 22:42:26
tags: 
- #atom
---
# Unsafe

Unsafe 对象提供了非常底层的，操作内存、线程的方法，Unsafe 对象不能直接调用，只能通过反射获得。

```java
public class UnsafeAccessor {
    static Unsafe unsafe;
 
    static {
        try {            
            Field theUnsafe = Unsafe.class.getDeclaredField("theUnsafe");
            theUnsafe.setAccessible(true);
            unsafe = (Unsafe) theUnsafe.get(null);
        } catch (NoSuchFieldException | IllegalAccessException e) {
            throw new Error(e);
        }
    }
 
    static Unsafe getUnsafe() {
        return unsafe;
    }
}
```

通过反射获取：

```java
import sun.misc.Unsafe;  
  
import java.lang.reflect.Field;  
  
public class Test18Unsafe {  
    public static void main(String[] args) throws NoSuchFieldException, IllegalAccessException {  
        Field theUnsafe = Unsafe.class.getDeclaredField("theUnsafe");  
        theUnsafe.setAccessible(true);  // 访问私有成员  
        Unsafe unsafe = (Unsafe) theUnsafe.get(null);  
        System.out.println(unsafe);  
    }  
}
```

## CAS操作

#TODO