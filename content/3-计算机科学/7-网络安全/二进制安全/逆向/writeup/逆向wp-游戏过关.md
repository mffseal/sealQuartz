---
title: 逆向wp-游戏过关
created: 2022-09-17 21:48:16
updated: 2022-09-17 22:05:54
tags: 
- article
---
# 逆向wp-游戏过关

bugku 逆向第三题.

http://gokoucat.ys168.com/

## 定位关键函数

通过对字符串 `done!!! the flag is` 进行交叉引用的定位, 找到关键函数的位置.

```c
...
    if ( byte_532E28[0] == 1
      && byte_532E28[1] == 1
      && byte_532E28[2] == 1
      && byte_532E28[3] == 1
      && byte_532E28[4] == 1
      && byte_532E28[5] == 1
      && byte_532E28[6] == 1
      && byte_532E28[7] == 1 )
    {
      sub_457AB4();  //关键函数
    }
```

## 分析函数

函数内部是对已有的数据进行处理并输出

## 控制程序流程

一种方法是, 利用 OD 调试, 然后控制跳转到 flag 处理函数, 直接输出:
1. 打开od, 加载程序
1. 在读取输入的地方设置断点:
    ```c
     while ( 1 )
    {
      s_print((int)"input n,n(1-8)\n", v19);
      sub_459418();
      s_print((int)"n=", v16);
      sub_4596D4("%d", (unsigned int)&v21);    //在这个位置设置断点
      s_print((int)"\n", v17);
      if ( v21 >= 0 && v21 <= 8 )
        break;
      s_print((int)"sorry,n error,try again\n", v19);
    }
    ```
1.双击修改 `call` 的地址到 flag 处理函数
1. 按 F8 执行修改过的指令
1. 返回控制台窗口, 查看输出

