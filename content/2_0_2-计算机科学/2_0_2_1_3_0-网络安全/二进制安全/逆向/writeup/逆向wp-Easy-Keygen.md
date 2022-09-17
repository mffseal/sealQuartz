---
title: 逆向wp-Easy-Keygen
created: 2022-09-17 21:41:11
updated: 2022-09-17 22:06:12
tags: 
- article
---
# 逆向wp-Easy-Keygen

基础的异或加密题.

http://gokoucat.ys168.com/

## 题目要求

Find the Name when the Serial is 5B134977135E7D13

## 黑盒测试

简单运行一下程序, 发现是 Windows 下的命令行程序, 要求输入 name 和 serial, 程序判断是否正确, 错误直接跳出.  

## 反编译

直接放 IDA 里反编译.

### 定位函数

通过搜索字符串 `Input Name:` 或`Input Serial:`, 查找交叉应用来定位主函数.

### 分析函数

这里没有什么坑, 找到主函数直接 F5 看 C 代码:  

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  signed int v3; // ebp@1
  signed int i; // esi@1
  int result; // eax@6
  char v6; // [sp+Ch] [bp-130h]@1
  char v7; // [sp+Dh] [bp-12Fh]@1
  char v8; // [sp+Eh] [bp-12Eh]@1
  char v9; // [sp+10h] [bp-12Ch]@1
  char v10; // [sp+11h] [bp-12Bh]@1
  __int16 v11; // [sp+71h] [bp-CBh]@1
  char v12; // [sp+73h] [bp-C9h]@1
  char v13; // [sp+74h] [bp-C8h]@1
  char v14; // [sp+75h] [bp-C7h]@1
  __int16 v15; // [sp+139h] [bp-3h]@1
  char v16; // [sp+13Bh] [bp-1h]@1

  v9 = 0;
  v13 = 0;
  memset(&v10, 0, 0x60u);
  v11 = 0;
  v12 = 0;
  memset(&v14, 0, 0xC4u);
  v15 = 0;
  v16 = 0;
  v6 = 16;
  v7 = 32;
  v8 = 48;
  sub_4011B9(aInputName);
  scanf(aS, &v9);
  v3 = 0;
  for ( i = 0; v3 < (signed int)strlen(&v9); ++i )
  {
    if ( i >= 3 )
      i = 0;
    sprintf(&v13, aS02x, &v13, *(&v9 + v3++) ^ *(&v6 + i));
  }
  memset(&v9, 0, 0x64u);
  sub_4011B9(aInputSerial);
  scanf(aS, &v9);
  if ( !strcmp(&v9, &v13) )
  {
    sub_4011B9(aCorrect);
    result = 0;
  }
  else
  {
    sub_4011B9(aWrong);
    result = 0;
  }
  return result;
}
```

#### 函数流程

1. 初始化字符串变量
1. 读入第一次输入
1. 循环遍历输入的每一个字符
    1. 将字符的 ASCII 数值与16, 32, 48 中的一个异或, key 的使用为 3 次一循环
    1. 结果储存为 16 进制, 不足 2 位则加入前导 0
1. 通过 `sprintf` 函数增量写入变量 v13 中
1. 读入第二次输入
1. 将 v13 的结果与输入比较, 一致则通过

#### 加密算法分析

函数通过一次 for 循环, 来遍历输入字符串的每一个字符, 通过 sprintf 格式化输入, 将按位异或的结果增量存入 v13 变量中.  
这里我们分析一下 `sprintf` 函数:  

> [参考文章](https://zh.cppreference.com/w/c/io/fprintf)  

```c
sprintf(&v13, aS02x, &v13, *(&v9 + v3++) ^ *(&v6 + i))
```

- 其中 aS02x 字符串的内容是 `%s%02x`, 指定格式化为字符串和 带前导 0 的 16 进制 2 位数
- `%s` 存入当前(也就是上一次异或结果) v13 变量的内容, 第二个
- `%02x` 存入 当前遍历字符与对应 KEY 异或的结果

```c
if ( i >= 3 )
      i = 0;
```

代表循环使用 3 个 KEY, 分别是16, 32, 48 (10进制表示).  

#### 破解算法

本题实际只是通过异或加密, 而异或运算的一个重要特点就是, 对一个数用同样的 KEY 异或 2 次, 会得到这个数本身.  
破解的方法就变得简单了, 只要再写一遍异或算法就行, 这里用 python 来写:  

```python
serial = "5B134977135E7D13"  ## 要解密的注册码
key = [16, 32, 48]           ## 异或用到的 key
name = ""                    ## 初始化

for i in range(len(serial) // 2):   
    each_2char = serial[i*2:i*2+2]  ## 将注册码两两分组
    name += chr(int(each_2char, 16) ^ key[i%3])  ## 异或运算
print(name)
```

注意, 加密算法保存的字符串格式为带前导 0 的 16 进制 2 位数, 所以反过来对注册码异或运算时, 要两两分组, 循环次数也要相应减半.  
`key[i%3]` 中的 `i%3` 则是使 3 个 key 循环使用.  