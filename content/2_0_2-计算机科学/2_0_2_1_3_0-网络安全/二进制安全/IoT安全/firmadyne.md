---
title: firmadyne
created: 2022-09-20 05:04:28
updated: 2022-09-20 05:06:48
tags: 
- atom
---

# firmadyne

Firmadyne是一款自动化和可裁剪的嵌入式Linux系统固件分析框架。它支持系统固件逆向QEMU嵌入式系统模拟执行。使用它模拟路由器固件执行路由器，然后可以基于模拟环境进行路由器漏洞挖掘、渗透攻防。

## 组件

- 修改过的便于防火墙程序执行的kernels (MIPS: [v2.6.32](https://github.com/firmadyne/kernel-v2.6.32),     ARM: [v4.1](https://github.com/firmadyne/kernel-v4.1), [v3.10](https://github.com/firmadyne/kernel-v3.10));  
- 一个用户空间的 [NVRAM library](https://github.com/firmadyne/libnvram)，用于模拟NVRAM硬件;  
- 一个固件提取器（[extractor](https://github.com/firmadyne/extractor)）， 用于提取嵌入式firmware固件的filesystem 和kernel;  
- 一个小[console](https://github.com/firmadyne/console)应用，用于另启一个shell进行调试;  
- 一个 [scraper](https://github.com/firmadyne/scraper)，用于下载 firmware固件（从 42+ 不同供应商）

## 参考

[(1条消息) 自动化固件逆向框架firmadyne使用详细教程_子曰小玖的博客-CSDN博客_firmadyne安装](https://blog.csdn.net/wxh0000mm/article/details/108443293)
[firmadyne/firmadyne: Platform for emulation and dynamic analysis of Linux-based firmware (github.com)](https://github.com/firmadyne/firmadyne)
