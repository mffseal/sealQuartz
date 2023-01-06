---
title: git中fork的仓库解决merge冲突
created: 2023-01-06 11:22:03
updated: 2023-01-06 13:36:57
tags: 
- article
- featured
---

# git中fork的仓库解决merge冲突

假设我们从远程主仓库repoA fork 了自己的repoB，我们开发并提交代码的时候，主仓库同时有其它人提交代码，不幸的是你们都修改了同一个文件的同一行，产生冲突。

## 1. 添加主仓库为upstream到本地git

[Git Upstreams and Forks: A Complete How-To | Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials/git-forks-and-upstreams)

1. 检查是否设置upstream仓库：

```bash
   git remote -v
   origin   git@bitbucket.org:my-user/some-project.git (fetch)
   origin  git@bitbucket.org:my-user/some-project.git (push)
```

如果如上述结果则说明没有设置upstream仓库，需要添加。

2. 设置upstream仓库

```bash
git remote add upstream git@bitbucket.org:some-gatekeeper-maintainer/some-project.git
```

添加后重新检查结果如下：

```bash
git remote -v
    origin    git@bitbucket.org:my-user/some-project.git (fetch) origin    git@bitbucket.org:my-user/some-project.git (push) upstream  git@bitbucket.org:some-gatekeeper-maintainer/some-project.git (fetch)
    upstream  git@bitbucket.org:some-gatekeeper-maintainer/some-project.git (push)
```

3. 创建分支或者使用dev分支，准备处理到来的冲突

fetch的最新代码，如果和本地提交修改了同一行，就会发生冲突，此时git的自动merge无法继续执行，需要手动处理冲突，为此创建一个分支而不是使用master分支来处理冲突。

```bash
git checkout -b dev
#some work and some commits happen
#some time passes
```

4. 从upstream fetch最新的代码

在不知不觉中，主仓库的其它开发人员会提交代码，你自己fork的代码可能就会落后，这时候需要fetch获取最新的代码到本地，保持代码的新鲜：

```bash
git fetch upstream
```

5. 合并本地仓库的head与主仓库的head

假如我们使用的是vscode来开发，有git图形界面。
fetch到最新的主仓库代码后，主仓库产生的变动会分成两种：
1. 没有冲突的代码更新，会直接被存放在staged changes中，代表这些变动无需处理冲突，可以直接在repoB上commit。
2. 存在冲突的更新，会存放在merge changes中，代表这些变动需要手动处理冲突，此时在vscode上通过图形界面手动审核代码处理冲突，完成处理后会移动到staged changes中。

6. push代码到克隆的远程仓库repoB

直接push就行。

```bash
git push
```

7. 向主仓库提交PR

此时在repoB上提交的commit是经过fetch最新代码并处理了合并冲突的，向主仓库提交合并请求不会再产生合并冲突问题。
