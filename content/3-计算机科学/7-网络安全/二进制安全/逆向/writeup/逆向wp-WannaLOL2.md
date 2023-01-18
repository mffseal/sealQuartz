---
title: 逆向wp-WannaLOL2
created: 2022-09-17 21:56:24
updated: 2022-09-18 22:13:42
tags: 
- article
- featured
---

# 逆向wp-WannaLOL2

逆向入门题.

题目在网络对应目录中: http://gokoucat.ys168.com/

## 黑盒测试

拿到题目第一步, 就是运行软件进行测试
- 判断软件平台
- 观察输入限制
- 观察输出信息

本题是一道 Windows 平台下的窗体程序, 任意输入内容进行测试:  

![[3-计算机科学/7-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917215724.png]]

随意输入后, 发现程序对输入的内容和长度没有做限制, 输入不通过时返回字符串 `error !`  
返回错的的字符串就是定位关键函数的一个突破点.  

## 反编译

使用 IDA 软件对程序进行反编译.  

```
无法确认程序位数时, 统一先用 X86 的 IDA 打开, 观察是否报错来确定是多少位的程序.
```

### IDA 视图配置

- 打开机器码显示
- 打开 16 进制视图 (Hex-View)
- 打开字符串视图 (Strings windows)

### 定位关键函数

通过输出字符串 `error !` 定位程序的关键函数.

#### 搜索字符串定位

1. 在 strings windows 中按 ctrl + F 搜索字符串 `error !`
1. 双击结果中匹配的内容, 跳转到对应的数据位置

#### 定位字符串引用位置

光标放在字符串的变量名处, 按 x 调出交叉应用窗口, 双击条目跳转到对应函数  

![[3-计算机科学/7-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917215738.png]]

引用位置:  

![[3-计算机科学/7-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917215748.png]]

### 花指令

#### 识别花指令

在关键函数处按 F5 发现无法转换成 C 代码, 判断函数中存在花指令.  

![[3-计算机科学/7-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917215712.png]]

这里是一种最基本的花指令类型, 文章 [代码混淆／程序保护（对抗反汇编）原理与实践](https://blog.csdn.net/pianogirl123/article/details/53871397) 介绍了基础的代码混淆知识, 可以扩展阅读.  

仔细分析本题的花指令:  

![[3-计算机科学/7-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917215802.png]]

第一和第二条的 `jz` 和 `jnz` 都跳转到了同一个地址, 那么代表程序真正执行起来, 无论如何都会跳转到指向的 `loc_401262+1` 位置.  
再观察 `loc_401262` 附近, 机器码是 `E8 66 B8 08 00`, 查询机器码对应的汇编指令, `E8` 值 `CALL`, 这样, IDA 错误的认为此处有 `CALL` 指令, 且后续的偏移量是一个无效的地址. 而程序执行时, 实际跳过了 `E8`.  

#### 处理花指令

本题的花指令有两种方法去除, 本质是让 IDA 不识别到 `E8` ([[3-计算机科学/3-操作系统/Linux/call|CALL]]).  

##### 替换指令为 `90`

`90` 机器码代表不执行任何动作, 将 `E8` 替换为 `90` 即可让 IDA 正确识别函数.  

光标定位到 `E8` 位置, 切换到 16 进制视图, 按 F2 开启编辑模式, 将 `E8` 改为 `90`, 再按 F2 保存更改.  

![[3-计算机科学/7-网络安全/二进制安全/逆向/writeup/z-attachments/flower3.gif]]

##### 将花指令标记为 db

光标定位到 `E8` 位置, 按 U (undefine), 选中下一个机器码 `66`, 按 C (code).  

![[3-计算机科学/7-网络安全/二进制安全/逆向/writeup/z-attachments/flower4.gif]]

#### 让 IDA 重新识别函数

将整个函数选中, 按 P 重新识别, 此时可以按 F5 转换为 C 代码了.  

![[3-计算机科学/7-网络安全/二进制安全/逆向/writeup/z-attachments/flower5.gif]]

### 主函数分析

IDA 生成的 C 代码如下:  

```c
int sub_4011F4()
{
  double v0; // st7@8
  double v1; // st6@8
  const CHAR *v3; // [sp-Ch] [bp-28h]@12
  const CHAR *v4; // [sp-8h] [bp-24h]@11
  CHAR String; // [sp+0h] [bp-1Ch]@1
  char v6; // [sp+1h] [bp-1Bh]@3
  char v7; // [sp+2h] [bp-1Ah]@4
  char v8; // [sp+3h] [bp-19h]@5
  int v9; // [sp+18h] [bp-4h]@8

  GetDlgItemTextA(hDlg, 1001, &String, 21);
  Sleep(0x1F4u);
  if ( strlen(&String) != 4 || String == 48 || v6 == 48 || v7 == 48 || v8 == 48 || String != 49 || v6 != 53 )
  {
    v4 = Caption;
LABEL_14:
    v3 = Text;
    return MessageBoxA(hWnd, v3, v4, 0);
  }
  v9 = v7 - 48;
  v0 = (double)v9;
  v9 = String - 48;
  v1 = (double)v9;
  v9 = v8 - 48;
  *(float *)&v9 = (v0 - v1 / (double)5) * (double)v9 * 16.0;
  if ( v8 != 48 && v8 == 48 )
    JUMPOUT(unk_4012AA);
  v4 = aCrackme2017Ctf;
  if ( *(float *)&v9 != 384.0 )
    goto LABEL_14;
  v3 = aRegistrationSu;
  return MessageBoxA(hWnd, v3, v4, 0);
}
```

#### 流程分析

分析代码, 可知程序通过对字符串数组 String, 也就是输入的内容进行条件比较, 再输出结果.  
其中 `Caption` 和 `aCrackme2017Ctf` 的内容是输出窗体的标题, `Test` 的内容为返回的 error 字符串, `aRegistrationSu` 的内容为输入内容正确回显的字符串.  
程序经过两次 if 判断, 来决定回显 error 还是 success:  

```c
if ( strlen(&String) != 4 || String == 48 || v6 == 48 || v7 == 48 || v8 == 48 || String != 49 || v6 != 53 )
```

为假, 且

```c
if ( v8 != 48 && v8 == 48 )
```

为真, 则返回 success.

#### 优化变量名

在用 IDA 分析代码时, 自动生成的变量名往往不能很好的表达变量的含义, 此时就需要手动重命名变量, 光标定位到对应变量后按 N 即可.  
对于部分数据, 可以右键转化为不同的显示方式, 如 48 重新显示为 字符 '0'.  
重新定义过变量名后的代码如下:  

其中 c1-c4 是输入字符串的 4 位字符

```c
int sub_4011F4()
{
  double v0; // st7@8
  double v1; // st6@8
  const CHAR *v3; // [sp-Ch] [bp-28h]@12
  const CHAR *v4; // [sp-8h] [bp-24h]@11
  CHAR c1; // [sp+0h] [bp-1Ch]@1
  char c2; // [sp+1h] [bp-1Bh]@3
  char c3; // [sp+2h] [bp-1Ah]@4
  char c4; // [sp+3h] [bp-19h]@5
  int temp; // [sp+18h] [bp-4h]@8

  GetDlgItemTextA(hDlg, 1001, &c1, 21);
  Sleep(0x1F4u);
  if ( strlen(&c1) != 4 || c1 == '0' || c2 == '0' || c3 == '0' || c4 == '0' || c1 != '1' || c2 != '5' )
  {
    v4 = str_title1;
LABEL_14:
    v3 = str_error;
    return MessageBoxA(hWnd, v3, v4, 0);
  }
  temp = c3 - '0';
  v0 = (double)temp;
  temp = c1 - '0';
  v1 = (double)temp;
  temp = c4 - '0';
  *(float *)&temp = (v0 - v1 / (double)5) * (double)temp * 16.0;
  if ( c4 != '0' && c4 == '0' )
    JUMPOUT(unk_4012AA);
  v4 = str_title2;
  if ( *(float *)&temp != 384.0 )
    goto LABEL_14;
  v3 = str_success;
  return MessageBoxA(hWnd, v3, v4, 0);
}
```

#### 主要语句分析

##### 第一处 if

```c
if ( strlen(&c1) != 4 || c1 == '0' || c2 == '0' || c3 == '0' || c4 == '0' || c1 != '1' || c2 != '5' )
```

解释一下:  

```
如果 (字符长度不等于4 或 第一个字符是0 或 第二个字符是0 或 第三个字符是0 或 第四个字符是0 或第一个字符不是1 或 第二个字符不是 5)
{
    返回 error
}
```

换句话说, 输入的字符串要为 4 个字符长度, 各字符不能是 '0', 第一个字符是 '1', 第二个字符是 '5'.

##### 第二处 if

此时, 我们知道:  

```c
c1 = '1'
c2 = '5'
```

还需要解出 c3 和 c4 的值, 即可. 分析第二处 if 前后的内容:  

```c
temp = c3 - '0';
  v0 = (double)temp;  // v0 = (double)c3
  temp = c1 - '0';
  v1 = (double)temp;  // v1 = 1
  temp = c4 - '0';   // temp = (int)c4
  *(float *)&temp = (v0 - v1 / (double)5) * (double)temp * 16.0;
  if ( *(float *)&temp != 384.0 )
    goto LABEL_14;
```

可知, `(v0 - v1 / (double)5) * (double)temp * 16.0` 的值等于 384 时, 可以返回 success. 其中 `v0` 是 `c3` 字符内容的浮点表示, `v1` 值是 1, `temp` 是 `c4` 内容的整数表示, 分别用 x 和 y 代替, 得到二元一次方程:  

$$(x - 1 / 5) \times y \times 16 = 384$$

化简一下后:  

$$(x - 1 / 5) \times y = 24$$

#### 解方程

用 python 或其他方式, 对二元一次方程求解:  

```python
for x in range(10):
    for y in range(10):
        if (x - 1 / 5) * y == 24:
            print(x,y)
```

解得 x 和 y 均为 5.  整个输入的字符串为1555.  输入求证:  

![[3-计算机科学/7-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917220053.png]]
