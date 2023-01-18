---
title: v2ray-multi最新版服务无法启动问题
created: 2023-01-12 16:45:35
updated: 2023-01-12 16:45:43
tags: 
- article
---

# v2ray-multi最新版服务无法启动问题

/etc/systemd/system/v2ray.service这个文件，ExecStart=/usr/bin/v2ray/v2ray -config /etc/v2ray/config.json，在-config前面加个run，然后systemctl daemon-reload，然后重启v2ray就行了。因为新版修改了启动命令，启动时需要加上run
