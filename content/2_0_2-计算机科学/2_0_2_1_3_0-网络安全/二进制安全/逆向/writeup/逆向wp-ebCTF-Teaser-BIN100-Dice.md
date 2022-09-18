---
title: 逆向wp-ebCTF-Teaser-BIN100-Dice
created: 2022-09-17 21:45:47
updated: 2022-09-18 20:48:52
tags: 
- article
- featured
---

# 逆向wp-ebCTF-Teaser-BIN100-Dice

[杭电 CTF 平台逆向第一题.](http://sec.hdu.edu.cn/question/reverse/5780?sort=default)

http://gokoucat.ys168.com/

## 定位关键函数

- 使用 IDA 字符串搜索
- 定位回显字符串被交叉引用的位置

得到关键函数中的重要片段如下: 

```c++
int __stdcall WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd)
{

  ......
  
  v9 = std::operator<<<std::char_traits<char>>(
         (int)&std::cout,
         "[*] You will first need to throw a three, press enter to throw a dice!");
  std::ostream::operator<<(v9, std::endl<char,std::char_traits<char>>);
  std::getline<char,std::char_traits<char>,std::allocator<char>>(&std::cin, &v83);
  v80 = time(0);  // 获取系统时间
  rand();    // 产生随机数
  v82 = 3;

......

  if ( v82 == 3 )     // 第一个为 3
  {
    fctx.call_site = 1;
    v10 = std::operator<<<std::char_traits<char>>((int)&std::cout, "[*] You rolled a three! Good!");
   
......

    v17 = std::operator<<<std::char_traits<char>>(
            (int)&std::cout,
            "[*] Next you will need to throw a one, press enter to throw a dice!");

    v80 = time(0);
    rand();
  
......

    if ( v82 == 1 )    // 第二个是1
    {
      fctx.call_site = 1;
      v18 = std::operator<<<std::char_traits<char>>((int)&std::cout, "[*] You rolled a one! Very nice!");
      
......

      v25 = std::operator<<<std::char_traits<char>>(
              (int)&std::cout,
              "[*] Next you will need to throw another three, press enter to throw a dice!");

      v80 = time(0);
      rand();
      
......

      if ( v82 == 3 )  // 第三个是3
      {
        fctx.call_site = 1;
        v26 = std::operator<<<std::char_traits<char>>((int)&std::cout, "[*] You rolled a three! Awesome!");
       
......

        v33 = std::operator<<<std::char_traits<char>>(
                (int)&std::cout,
                "[*] Throw another three for me now, press enter to throw a dice!");

        v80 = time(0);
        rand();
        
......

        if ( v82 == 3 )  // 第四个是3
        {

......

          v42 = std::operator<<<std::char_traits<char>>(
                  (int)&std::cout,
                  "[*] The last character you need to roll is a seven....  (o_O)  Press enter to throw a dice!");

          v80 = time(0);
          
......

          if ( v82 == 7 )   //第五个是7
          {
            fctx.call_site = 1;
            v43 = std::operator<<<std::char_traits<char>>(
                    (int)&std::cout,
                    "[*] You rolled a seven, with a six sided dice! How awesome are you?!");

......

            fctx.call_site = 1;
            if ( std::string::find((std::string *)&v84, "ebCTF", 0) == -1 )
            {
              fctx.call_site = 1;
              v59 = std::ostream::operator<<(&std::cout, std::endl<char,std::char_traits<char>>);
              v60 = std::operator<<<std::char_traits<char>>(
                      v59,
                      "[!] It seems you did something wrong :( No flag for you.");
              
......

            }
            else
            {
              v55 = std::operator<<<std::char_traits<char>>(
                      (int)&std::cout,
                      "[*] You rolled 3-1-3-3-7, what does that make you? ELEET! \\o/");    //这里也可以得知过关顺序
              std::ostream::operator<<(v55, std::endl<char,std::char_traits<char>>);
              v56 = std::operator<<<std::char_traits<char>>((int)&std::cout, "[*] Nice job, here is the flag: ");
              
......

            }
          }
         
......

}
```

## 分析函数

- 函数通过 rand() 函数产生随机数
- 通过随机数投掷骰子
- 骰子的顺序为 3-1-3-3-7 则过关返回 flag

## 调试程序

使用 OD 调试程序, 这里复习一下 OD 的使用:
- 键入 bp xxx 则在 xxx位置下断点
- F9 为继续运行到断点处
- F8 为单步步过
- F7 为单步步入
- F4 为运行到光标处
- F2 为在光标位置切换断点
- 双击汇编指令或按空格可修改指令
- 双击寄存器可修改寄存器数据
- 双击栈后空格可修改栈中数据

### 修改寄存器尝试过关

因为每次都是随机产生数字, 而且将处理完的数据保存在 `EAX` 寄存器用于投掷骰子, 那么可以修改 `EAX` 内容来实现精准投掷.  

![[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220918204747.png]]

- 将 EAX 的数字分别修改为 3, 1, 3, 3, 操作重复 4 次即可
- 此时发现, 第五个 7 不是通过寄存器来取值的, 而是通过栈取值

![[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220918204801.png]]

- 观察后续代码, 发现有大量对栈 [ebp-0x5c] 位置的 cmp (比较) 操作
- 可以大胆猜测程序用 7 对 [ebp-0x5c] 比较, 真则投掷出 7 点
- 此时的 ebp 为 `0028FEC8`
- [ebp-0x5c] 则为 `0028FE6C`
- 修改此处栈值为 7

![[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220918204815.png]]

继续执行程序, 确实投掷出了 7 点, 但是程序似乎还有一个检测机制, 阻止了我们获取 flag.  

![[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220918204839.png]]

### 利用 IDA 修改程序

#### 思路

- 回想程序的代码, 调用的 `time()` 函数
- 大胆猜测, 程序应该是利用各处 `time()` 获取的系统时间, 来检测程序是不是在被调试.
- 因此, 可用 IDA 修改程序指令, 来让程序一次通过.

在 OD 调试的时候, 记录下 5 次投掷的位置:

```
00401830  --> 3
00401B6E  --> 1
00401EAA  --> 3
004021DA  --> 3
0040254E  --> 7
```

IDA 中的操作:
- 按 G 可打开地址跳转窗口
- 修改: Edit -- Patch program -- Change byte...
- 应用修改到文件: Edit -- Patch program -- Apply patches to input file...
- 主要要用 90 (nop) 来填充剩余空间 (00也可以)

#### 操作细节

- 这里我们将取值部分的操作修改为直接为 eax 赋目标数值, 同时对 ecx 赋值 [目标数值 - 1] 的值
- 第五次则是对 [ebp-0x5c] 处赋值 7

可以利用网络或其他工具, 或者是 OD (OD 可以直接编辑汇编代码, 然后观察对应机器码即可), 得到目标机器码:  

```
mov ecx, [num]   -->   B9 [num] 00 00 00
mov eax, [num]   -->   B8 [num] 00 00 00
例如: mov ecx, 2 -->  B9 02 00 00 00

mov [ebp+var_5C], 7  -->  C7 45 A4 07 00 00 00
```

前 4 次修改前:  

![[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917214627.png]]

前 4 次修改后:  

![[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917214643.png]]

第 5 次修改前:  

![[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917214657.png]]

第 5 次修改后:  

![[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917214710.png]]

Apply patches to input file 后即大功告成.

## 执行结果

值得注意的是, 程序最后运行结束会直接关闭, 所以我们要先打开 cmd, 再用 cmd 打开程序:

![[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/逆向/writeup/z-attachments/Pasted image 20220917214722.png]]
