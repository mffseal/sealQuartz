---
title: PKI
created: 2022-09-28 00:36:58
updated: 2022-09-28 20:19:51
tags: 
- article
---

# PKI

Public Key Infrastructure，公钥基础设施。

## 组成

一个PKI体系由终端实体、证书认证机构、证书注册机构和证书/[[2-数学/2-密码学/CRL|CRL]]存储库四部分共同组成。

- 证书颁发机构（[[2-数学/2-密码学/CA|CA]]）
- 证书注册机构（[[2-数学/2-密码学/RA|RA]])
- 证书库
- 密钥备份及恢复系统
- 证书废除处理系统
- 应用系统接口
- [[2-数学/2-密码学/数字证书|数字证书]]

## 重要角色

1. 终端实体（EE, End Entity）: 证书的最终使用者，例如总部和分支的网关。
2. 证书颁发机构（CA， Certificate Authority）：是一个权威的、可信的第三方机构，负载[[2-数学/2-密码学/证书颁发|证书颁发]]、查询以及更新等工作。
3. 证书注册机构（RA）
