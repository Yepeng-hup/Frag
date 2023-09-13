## Frag

### 背景

由于公司需要记录一些资源、维护记录等，以及过多的系统URL。以前，这一切都是手动记录在本子上，而且非常混乱。随着时间的推移，它在哪里变得不清楚了。正好自学了点Python<菜鸡水平>，开发这个简单的记录碎片系统。刚刚入门python的伙计也可以把Frag当做入门系统学习。技术难度不是很难。

### 技术使用

python3.7, js, css, html, shell, docker, k8s

### Frag 介绍

该系统主要可以记录维护、服务器协作、事件、检查, 安全等。它还可以上传文件、远程执行代码、集成多个系统url、界面操作Redis(只实现了list和str数据类型，其他数据类型后面会实现。)、Webhook、用户锁、用户权限和简单的技术文档编写等web操作。支持Docker、K8S部署，如果有其他要求，支持二次开发。

### Frag 运行

更新 frag.yaml 配置文件 , 登录用户: admin    登录密码: frag

```bash
Linux: bash frag_tp.sh start
win: python frag_run.py
```



![](https://s1.ax1x.com/2023/04/06/ppoQEtA.png)

![](https://s1.ax1x.com/2023/04/11/ppLoRXT.png)





