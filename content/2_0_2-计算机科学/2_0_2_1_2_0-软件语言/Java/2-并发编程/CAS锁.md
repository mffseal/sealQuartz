---
title: CAS锁
created: 2022-06-02 14:21:16
updated: 2022-06-02 14:21:55
tags: 
- atom
---
# CAS锁

利用原子类配合cas操作组成标志位，来模拟锁：

```java
// 不要用于实践！！！
public class LockCas {
    private AtomicInteger state = new AtomicInteger(0);
 
    public void lock() {
        while (true) {
            if (state.compareAndSet(0, 1)) {
                break;
            }
        }
    }
 
    public void unlock() {
        log.debug("unlock...");
        state.set(0);
    }
}
```