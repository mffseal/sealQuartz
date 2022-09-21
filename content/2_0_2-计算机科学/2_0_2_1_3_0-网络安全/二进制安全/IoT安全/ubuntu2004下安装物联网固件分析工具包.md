---
title: ubuntu2004下安装物联网固件分析工具包
created: 2022-09-20 05:02:38
updated: 2022-09-20 23:30:00
tags: 
- article
---

# ubuntu2004下安装物联网固件分析工具包

## 基础环境

系统：ubuntu2004 64位。
代理工具：proxychains4。
宿主机网络加速软件开放端口用于给虚拟机代理。

## 安装流程

1. 安装代理工具：`sudo apt install proxychains4`。
2. 配置代理：`sudo vim /etc/proxychains4.conf`，将最后的代理服务器地址换成`socks5 宿主机Ip 代理端口`
3. 克隆自动化分析工具包脚本项目：`git clone --recursive https://github.com/attify/firmware-analysis-toolkit.git`。
4. 手动安装binwalk。
5. 手动[[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/IoT安全/安装qemu|安装qemu]]。
6. 手动安装[[2_0_2-计算机科学/2_0_2_1_3_0-网络安全/二进制安全/IoT安全/firmadyne|firmadyne]]。
7. 安装firmware-analysis-toolkit剩余部分。

## 参考

[路由器固件模拟环境搭建(超详细)_Tig3rHu的博客-CSDN博客_路由器环境搭建](https://blog.csdn.net/wuyou1995/article/details/105545581?spm=1001.2014.3001.5502)
