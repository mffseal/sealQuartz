---
title: 逆向wp-reverse02
created: 2022-09-17 21:53:22
updated: 2022-09-17 21:55:37
tags: 
- article
---
# 逆向wp-reverse02

[杭电 CTF 平台逆向第三题.](http://sec.hdu.edu.cn/question/reverse/5786?sort=default)  

题目在网络对应目录中: http://gokoucat.ys168.com/

## 定位函数
程序时一个 win32 的窗口程序, 按钮是灰色的.  
老套路, 根据字符串来定位函数.  

这题可以找到一个内容是 `flag:{NSCTF_md57e0cad17016b0>?45?f7c>0>4a>1c3a0}` 的字符串, 直接提交错误, 看来没这么简单.  

### 交叉引用

对该字符串的交叉引用有两处, 分别分析发现其中一个应该为主要的函数:

```c
int __thiscall sub_401070(_BYTE *this)
{
  int v1; // edx
  int v2; // esi
  int result; // eax

  if ( ((unsigned __int8)byte_403028 ^ 7) != *this
    || ((unsigned __int8)byte_403027 ^ 7) != this[1]
    || ((unsigned __int8)byte_403026 ^ 7) != this[2]
    || ((unsigned __int8)byte_403025 ^ 7) != this[3]
    || ((unsigned __int8)byte_403024 ^ 7) != this[4]
    || ((unsigned __int8)byte_403023 ^ 7) != this[5]
    || ((unsigned __int8)byte_403022 ^ 7) != this[6] )
  {
    v1 = dword_403380;
    v2 = dword_403018;
  }
  else
  {
    v1 = dword_403380 + 2;
    v2 = dword_403018 - 1;
    dword_403380 += 2;
    --dword_403018;
  }
  if ( ((unsigned __int8)byte_403021 ^ 0x33) == this[7]
    && ((unsigned __int8)byte_403020 ^ 0x33) == this[8]
    && ((unsigned __int8)byte_40301F ^ 0x33) == this[9]
    && ((unsigned __int8)byte_40301E ^ 0x33) == this[10]
    && ((unsigned __int8)byte_40301D ^ 0x33) == this[11]
    && ((unsigned __int8)byte_40301C ^ 0x33) == this[12] )
  {
    --v1;
    v2 += 2;
    dword_403380 = v1;
    dword_403018 = v2;
  }
  if ( v2 + v1 == 3 )
    result = sub_401000();
  else
    result = MessageBoxA(0, "flag:{NSCTF_md57e0cad17016b0>?45?f7c>0>4a>1c3a0}", "Flag", 0);
  dword_403018 = 1;
  dword_403380 = 0;
  return result;
}
```

看来程序是对一串字符串做异或, 然后判断和输入的内容是否一致, 一致则返回处理过后的真正的 flag.

## 解密

众所周知, 重复两次异或, 就是原结果, 将上述代码中的内置字符拷贝出来, 再仿照其异或的过程进行解密:

```python
key1 = [0x4e, 0x62, 0x57, 0x47, 0x39, 0x3b, 0x32]
key2 = [0x6a, 0x58, 0x6a, 0x46, 0x50, 0x4a]
for i in key1:
    print(chr(i ^ 0x7), end="")
for j in key2:
    print(chr(j ^ 0x33), end="")

```

输出结果为: `IeP@><5YkYucy`

## 灰色按钮

程序的按钮是灰色的不可点击, 用灰色按钮克星等程序, 破解按钮.

![[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917215523.png]]

具体的实现过程有待研究...  

## 输出答案

输入之前解密的 key `IeP@><5YkYucy` 即可:  

![[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917215533.png]]