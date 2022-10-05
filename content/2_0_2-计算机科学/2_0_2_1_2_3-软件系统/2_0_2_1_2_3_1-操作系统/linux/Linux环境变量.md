---
title: Linux环境变量
created: 2022-10-05 22:01:24
updated: 2022-10-05 22:07:50
tags: 
- atom
---

# Linux环境变量

每个进程都有一个属于自己的环境变量列表。进程使用这些变量的值去使用系统提供的资源。本节主要介绍使用库函数操作进程的环境变量。

```
char *getenv(const char *name);

功能：获取环境变量name的值

参数：name 指定环境变量的名字。

返回值：成功   返回环境变量name的值的首地址    
		返回NULL    代表没有找到这个环境变量
		
int putenv(char *string);

     功能：将字符串设置为进程的环境变量

     参数：string 以格式name=value的字符串，将这个字符串设置到进程的环境变量列表中。  如果进程中有和name同名的环境变量，则使用value的值替换掉原来的值。如果没有  同名的环境变量，则将字符串设置为进程的环境变量

     返回值：成功   返回 0    

        错误   返回非0    errno被设置为相应的错误值

切记：只是将字符串设置到进程环境变量列表中，而不是拷贝。如果string指向的字符串的内容改变，则值做相应的改变

      int setenv(const char *name, const char *value, int overwrite);

     功能：如果环境变量存在，根据overrite的值对环境变量操作。如果不存在，创建环境变量

     参数：name  环境变量的名字

     value  环境变量的值

     overwrite  0  如果环境变量已经在列表中，不改变环境变量的值

          非0  如果环境变量已经在列表中，使用value的值替换掉原来的值

     返回值：成功   返回 0    

        错误   -1   errno被设置为相应的错误值

    int unsetenv(const char *name);

     功能：从环境变量列表中删除环境变量，如果环境变量不存在，什么都不做

     参数：name  环境变量的名字

     返回值：成功   返回 0    

        错误   -1   errno被设置为相应的错误值

     int clearenv(void);

    功能：清除进程的环境变量列表并将全局变量environ设置为NULL。

     返回值：成功    0      错误   非0
```
