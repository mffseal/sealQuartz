---
title: 逆向wp-keylead
created: 2022-09-17 21:49:21
updated: 2022-09-17 21:51:25
tags: 
- article
---
# 逆向wp-keylead

[杭电 CTF 平台逆向第二题.](http://sec.hdu.edu.cn/question/reverse/5783?sort=default)

题目在网络对应目录中: http://gokoucat.ys168.com/

## 文件分析

通过在 lunux 环境下, 使用 `file keylead` 发现是一个压缩文件, 解压后得到可执行文件.

```shell
file keylead

keylead: XZ compressed data
```

## 函数分析

通过字符串定位的方法, 找到主函数.

### 主函数

```c
signed __int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  unsigned int v3; // eax
  unsigned int i_rand_n1; // ST14_4
  signed __int64 result; // rax
  unsigned int i_rand_n5; // [rsp+4h] [rbp-1Ch]
  unsigned int i_rand_n4; // [rsp+8h] [rbp-18h]
  unsigned int i_rand_n3; // [rsp+Ch] [rbp-14h]
  unsigned int i_rand_n2; // [rsp+10h] [rbp-10h]
  int start_time; // [rsp+18h] [rbp-8h]

  puts("hi all ----------------------");
  puts("Welcome to dice game!");
  puts("You have to roll 5 dices and get 3, 1, 3, 3, 7 in order.");
  puts("Press enter to roll.");
  getchar();
  v3 = time(0LL);
  srand(v3);
  start_time = time(0LL);                       // 获取基准时间
  i_rand_n1 = rand() % 6 + 1;
  i_rand_n2 = rand() % 6 + 1;
  i_rand_n3 = rand() % 6 + 1;
  i_rand_n4 = rand() % 6 + 1;
  i_rand_n5 = rand() % 6 + 1;
  printf("You rolled %d, %d, %d, %d, %d.\n", i_rand_n1, i_rand_n2, i_rand_n3, i_rand_n4, i_rand_n5);
  if ( i_rand_n1 != 3 )
    goto LABEL_20;
  if ( time(0LL) - start_time > 2 )             // 超时则失败, 估计时防调试的手段
  {
    puts("No cheat!");
    return 0xFFFFFFFFLL;
  }
  if ( i_rand_n2 != 1 )
    goto LABEL_20;
  if ( time(0LL) - start_time > 2 )
  {
    puts("No cheat!");
    return 0xFFFFFFFFLL;
  }
  if ( i_rand_n3 != 3 )
    goto LABEL_20;
  if ( time(0LL) - start_time > 2 )
  {
    puts("No cheat!");
    return 0xFFFFFFFFLL;
  }
  if ( i_rand_n4 != 3 )
    goto LABEL_20;
  if ( time(0LL) - start_time > 2 )
  {
    puts("No cheat!");
    return 0xFFFFFFFFLL;
  }
  if ( i_rand_n5 != 7 )
  {
LABEL_20:
    puts("You DID NOT roll as I said!");
    puts("Bye bye~");
    result = 0xFFFFFFFFLL;
  }
  else if ( time(0LL) - start_time <= 2 )
  {
    puts("You rolled as I said! I'll give you the flag.");
    f_cal_flag();                               // 计算并返回flag的函数
    result = 0LL;
  }
  else
  {
    puts("No cheat!");
    result = 0xFFFFFFFFLL;
  }
  return result;
}
```

- 函数通过 `rand()`, 随机生成 5 个数字用于投掷骰子
- 有防调试修改的手段
- 结果为 31337 则调用 flag 生成的函数 `f_cal_flag()`

### flag 生成函数

尝试通过对 flag 生成函数进行还原, 得到flag, 复制代码后修改执行:

```c
#include<stdio.h>

int main(void)
{
  int v0; // ST0C_4
  int v1; // ST08_4
  int v2; // ST0C_4
  int v3; // ST0C_4
  int v4; // ST08_4
  int v5; // ST0C_4
  int v6; // ST08_4
  int v7; // [rsp+8h] [rbp-8h]
  int v8; // [rsp+8h] [rbp-8h]
  int i; // [rsp+8h] [rbp-8h]
  int j; // [rsp+8h] [rbp-8h]
  int v11; // [rsp+Ch] [rbp-4h]
  int v12; // [rsp+Ch] [rbp-4h]
  int v13; // [rsp+Ch] [rbp-4h]
  int v14; // [rsp+Ch] [rbp-4h]
  int v15; // [rsp+Ch] [rbp-4h]
  int v16; // [rsp+Ch] [rbp-4h]

  v11 = 0;
  v7 = 0;
  
char flag[] = 
{0x41,0x00,0x61,0x00,0x63,0x00,
 0x62,0x00,0x65,0x00,0x66,0x00,
 0x49,0x00,0x33,0x00,0x31,0x00,
 0x30,0x00,0x53,0x00,0x32,0x00,
 0x37,0x00,0x36,0x00,0x39,0x00,
 0x38,0x00,0x7b,0x00,0x7d,0x00,};
  
  while ( v11 != 1 )
  {
    putchar(flag[14 * v11++]);
    do
    {
      while ( v7 <= 1 )
        putchar(flag[20 * v11 - 8 * v7++]);
      v1 = v7 + 1;
      v2 = 3 * v11;
      putchar(flag[2 * v2 + 11 + v1]);
      v2 *= 5;
      v8 = v1 - 1;
      putchar(flag[2 * v2 + v8]);
      v12 = v2 / 3;
      while ( 1 )
      {
        while ( 1 )
        {
LABEL_12:
          if ( !v8 )
          {
            putchar(flag[2 * v12]);
            v15 = v12 ^ 2;
            while ( 2 )
            {
              for ( i = 1; i <= 9; ++i )
                putchar(flag[10 * (i % 2) + 3 + v15]);
              v13 = v15 + 1;
LABEL_44:
              putchar(flag[v13 / 3]);
              if ( i == 10 )
              {
                v13 += 2 * v13 + 13;
                i = 19;
                goto LABEL_33;
              }
              if ( i == 2 )
              {
                i = v13-- + 2;
                goto LABEL_4;
              }
              if ( (unsigned int)(i - 22) <= 0xA )
              {
                v14 = v13 - 3;
                for ( j = i - v14; ; j = 8 )
                {
LABEL_58:
                  putchar(flag[v14 + 1]);
                  v16 = v14 + 1;
                  if ( j == 11 )
                  {
                    v13 = (v16 + 14) / 2;
                    i = 11 * (v13 / 6);
                    goto LABEL_44;
                  }
                  if ( j != 13 )
                    break;
                  v12 = v16 + 8;
                  v8 = 2;
LABEL_51:
                  while ( 2 )
                  {
                    putchar(flag[v12 - 10]);
                    if ( v8 == v12 )
                    {
                      v4 = v8 + 2;
                      v5 = v12 + 2;
                      putchar(flag[v5 / 2 + v4 / 5]);
                      i = v4 / 2;
                      putchar(flag[i / 5 + v5]);
                      v13 = v5 + i - 1 + v5;
                      while ( 1 )
                      {
LABEL_33:
                        putchar(flag[v13 - 19]);
                        if ( i == 2 )
                        {
                          v3 = v13 + 1;
                          putchar(flag[v3 / 2 - 3]);
                          v13 = v3 / 5 + 2;
                          i = 2;
                          goto LABEL_44;
                        }
                        if ( i <= 2 )
                          break;
                        if ( i == 10 )
                        {
                          v12 = v13 - 31;
                          v8 = 9;
                          goto LABEL_51;
                        }
                        if ( i != 19 )
                          goto LABEL_44;
                        i = 2;
                      }
                      if ( i == 1 )
                      {
                        v8 = 17;
                        v12 = v13 % 5 - 17 + v13;
LABEL_20:
                        putchar(flag[v12 - v8 + 9]);
                        v12 += ~v8++;
                        continue;
                      }
                      goto LABEL_44;
                    }
                    break;
                  }
                  if ( v8 != 9 )
                  {
                    if ( v8 != 2 )
                      goto LABEL_12;
                    j = 2;
                    v16 = v12 - 18;
LABEL_64:
                    v6 = 9 * j;
                    putchar(flag[v16 / 2 + v6 + v6 % 10]);
                    v11 = v16 + 1;
                    v7 = v6 % 10;
                    goto LABEL_21;
                  }
                  putchar(flag[v12 - 16]);
                  v14 = v12 / 2;
                }
                if ( j == 8 )
                {
                  v15 = v16 + 1;
                  i = 7;
                  continue;
                }
                goto LABEL_64;
              }
              goto LABEL_4;
            }
          }
          if ( v8 == 2 )
            break;
          if ( v12 == 7 )
          {
            putchar(flag[21 - v8]);
            v13 = 49;
            i = v8 / 3;
            goto LABEL_33;
          }
          if ( v8 != 3 )
            goto LABEL_20;
          putchar(flag[2 * (v12 / 3)]);
          v13 = v12 / 3;
          i = 9;
          do
          {
            while ( 1 )
            {
              if ( v13 == 10 )
              {
                putchar(flag[i + 8]);
                v14 = 9;
                j = i + 1;
                goto LABEL_58;
              }
              if ( v13 == 11 )
              {
                putchar(flag[i / 7]);
                v13 = i-- - 11;
              }
LABEL_4:
              if ( i != 9 )
                break;
              putchar(flag[v13 * v13 + 7]);
              v13 = v13 * v13 + 1;
              i = 10;
            }
          }
          while ( i != 13 );
          putchar(flag[2 * v13 + 12]);
          v8 = 3;
          v12 = 3 * v13;
        }
        putchar(flag[3 * v12 + 1]);
        v0 = v12 * v12;
        putchar(flag[v0 - 15]);
        v11 = v0 - 15;
        v7 = 4;
        putchar(flag[4]);
LABEL_21:
        if ( v7 != 4 )
          break;
        putchar(flag[v11 + 6]);
        v12 = v11 - 3;
        v8 = 3;
      }
    }
    while ( v7 != 8 );
    putchar(flag[2 * v11 + 32]);
  }
  
  return 0;
}
```

执行返回的结果为:  

```
ASIS{1fc1089e328eaf737373737c882ca0b10fcfe6}
```

看似正确, 但实际上有错误, 对比答案并调试后发现, 59 行处多次循环, 导致 flag 中 7373 处多了.  
这个问题暂时没有想明白.

## 方法分析

利用程序开始的调用逻辑, 直接执行 flag 生成函数.

### 定位程序起始位置

在左侧函数表双击定位到 start

![[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917215125.png]]

```
参考1 [main() 函数在 Linux 上的启动过程分析 ](http://gokoucat.cn/2018/10/01/security/reverse/learning/main-function-startup-process-on-linux/)  
参考2 [x86-64 框架下的参数传递](http://gokoucat.cn/2018/10/01/security/reverse/learning/64-calling-convention/)  
```

通过修改 `mov     rdi, offset main ; main` 指令的目标位置, 即可控制程序跳转到 flag 生成函数.

### 函数位置记录

- `mov     rdi, offset main` 在 `0x4005dd`
- `f_cal_flag` 在 `0x4006b6`

因此只要将 `mov     rdi, offset main` 修改为 `mov     rdi, 0x4006b6` 即可.  

## 调试

### gdb 操作复习

- 开始调试 `gdb xxx`
- 设置断点 `b *0x111111`
- 查看断点: `i b`
- 删除断点: `d xx`
- 运行: `r`
- 继续执行到断点: `c`
- 查看寄存器: `i r` 或 `i registers`
- 修改寄存器值: `set $REGISTER=VALUE`

### 开始调试

```sh
gdb keylead            ## 进入调试环境
b *0x4005dd            #设置断点
r                      #运行程序
i r                   #查看寄存器的值
n                     #单步运行
i r                   #查看寄存器的值
set $rdi=0x4006b6    #设置 rdi寄存器的值
c                    #继续运行程序
```

返回flag: `ASIS{1fc1089e328eaf737c882ca0b10fcfe6}`