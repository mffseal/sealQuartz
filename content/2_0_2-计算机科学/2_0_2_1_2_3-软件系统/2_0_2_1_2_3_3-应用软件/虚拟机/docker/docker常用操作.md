---
title: docker常用操作
created: 2022-11-17 14:46:18
updated: 2022-11-28 16:31:11
tags: 
- article
---

# docker常用操作

## 查询正在运行容器并进入

```shell
sudo docker ps  
sudo docker exec -it 775c7c9ee1e1 /bin/bash
```

## 启动容器

```bash
docker run -itd -p [外部端口]:[内部端口] -v [外部绝对路径]:[内部绝对路径] -w [工作路径] --name [自定义名称] [镜像名]:[版本号] /bin/bash
```

例子

```bash
docker run -itd -p 4222:22 -v /root/mfjshared:/root/shared -v /root/jys:/root/jys -w /root --name edge-dev-env-49-mfj edge-dev-env:v4.9 /bin/bash
```

## 打包容器成镜像

```bash
docker commit -a "[作者名称]" -m "[描述]" [容器id] [镜像名称]:[版本号]
```
