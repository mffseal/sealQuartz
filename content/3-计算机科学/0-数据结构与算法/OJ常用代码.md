---
title: OJ常用代码
created: 2022-09-18 00:32:03
updated: 2022-09-18 00:32:34
tags: 
- article
---
# OJ常用代码

## 进制转换

### 任意进制转 10 进制

对于一个 p 进制的 n 位数 y 来说, 其每一位$a_n$的关系是
$$
y = a_1 \times p^{n-1} + n_2 \times p^{n-2} + ... + a_{n-1} \times p^1 + a_n \times p^0
$$

转换代码实现:

```c++
#include <iostream>
using namespace std;

int main(void)
{
	int y = 0, a = 0, p = 1, result = 0;  // p 初始为1, 代表p^0 
	cin>>y>>a;
	while (y!=0)
	{
	    result += (y % 10) * a;  // 将最低位乘以p^n 再累加 
	    y /= 10;  //每次去掉最低位 
	    p *= a;  // 次数递增 
    }
    cout<<result;
	return 0;
}
```

### 10 进制转任意进制

采用除基取余法:
- 基代表目标进制 q

步骤:
1. 每次将上一步的商除以目标进制 q
1. 余数插入结果, 从左向右插入
1. 直到商为 0 , 插入本次余数后停止

代码实现(10进制数 y 转化为 q 进制数):

```c++
#include <iostream>
using namespace std;

int main(void)
{
	int y = 0, q = 0, p = 1;
    string result; 
	cin>>y>>q;
	/* 商为0则停止, 为了保证最后一次余数的存储, 用 do..while */
	do
	{
	    string str = to_string(y%q);  // 对 q 取余 
	    result.insert(0, str);
	    y /= q;
    } while(y!=0);
    
    cout<<result;
	return 0;
}
```

### 任意进制间转换

将上面两个步骤结合起来即可.

## 最小公因数

递归实现:

```c++
#include <iostream>
using namespace std;

int gcd(int a, int b)
{
    return b==0 ? a : gcd(b, a%b);
}
```

## 互质

判断两个数互质或者是分数的化简:
- 就是判断两个数的最小公因数是不是1

## 最小公倍数

a,b两数求最小公倍数:
1. 先求它们的最小公因数gcd
1. 再算 $a * b / gcd$


## 排序

### 冒泡排序

[[3-计算机科学/0-数据结构与算法/冒泡排序|冒泡排序]]

1. 有n个元素则循环n-1次
1. 好像传手帕一般, 每次将当前为固定数中最大的那个传到右边固定
1. 最后一步则是根据情况交换第一和第二个元素

```c++
#include <iostream>
using namespace std;

int main(void)
{
	int a[5] = {3,1,4,5,2};
	int n = sizeof(a) / 4;  // 元素个数 
	for (int i=0; i<n-1; i++)
	{
	    /* n个元素总共执行n-1次 */ 
	    for (int j=0; j<n-1-i; j++)
	    {
	        int temp;
	        /* 左大于右则交换为升序 */
	        /* 每一轮遍历都是将为固定中最大的移到右边固定 */ 
	        if (a[j]>a[j+1])
	        {
	            temp = a[j];
	            a[j] = a[j+1];
	            a[j+1] = temp;
            }
        }
    }
    for (int i=0; i<n; i++)
    {
        printf("%d ", a[i]);
    }
	return 0;
}
```

### 简单选择排序

1. 外围循环为当前最小交换位标记
1. 内层循环每次把当前最小的和标记位互换
    1. 内循环结束一轮时标记位为当前子序列中最小的
1. 依次从小到大放到左边

实现:

```c++
#include <iostream>
using namespace std;

int main(void)
{
	int a[5] = {3,1,4,5,2};
	int n = sizeof(a) / 4;  // 元素个数 
	for (int i=0; i<n; i++)  // 其实i<n-1即可
	{
	    for (int j=i+1; j<n; j++)
	    {
	        int temp;
	        if (a[i]>a[j])
            {
                temp = a[i];
                a[i] = a[j];
                a[j] = temp;
            }
        }
    }
    for (int i=0; i<n; i++)
    {
        printf("%d ", a[i]);
    }
	return 0;
}
```

### 直接插入排序

1. 将第一个元素当作初始有序子序列, 从第二个元素开始遍历
1. 暂存当前元素值
1. 从当前遍历元素开始往回(左)遍历, 如果比当前元素小则往右挪
    1. 如果挪动, 自然会覆盖掉当前元素的坑位
1. 当前元素插入挪出的坑位, 左侧子序列还保持有序

实现:

```c++
#include <iostream>
using namespace std;

int main(void)
{
	int a[5] = {3,1,4,5,2};
	int n = sizeof(a) / 4;  // 元素个数 
	for (int i=1; i<n; i++)
	{
	    int temp = a[i];
	    int j = i;
	    /* 将比当前数字大的数往右移动一个, 给当前数留出坑位 */
	    /* 左侧序列保持有序, 所以一旦不大于当前数则不用继续遍历了 */ 
	    for (; j>=0 && a[j-1]>temp; j--)
        {
            a[j] = a[j-1];
        }
        a[j] = temp;   // 当前数插入坑位 
    }
    for (int i=0; i<n; i++)
    {
        printf("%d ", a[i]);
    }
	return 0;
}
```

### 2路归并排序

#### 递归版

```c++
#include <iostream>
using namespace std;

void merge(int a[], int l1, int r1, int l2, int r2);
void sort_merge(int a[], int left, int right);

int main(void)
{
	int a[6] = {5,2,4,1,3,6};
	for (int i=0; i<6; i++)
	{
	    printf("%d ", a[i]);
    }
	printf("\n");
	sort_merge(a, 0, 5);
	for (int i=0; i<6; i++)
	{
	    printf("%d ", a[i]);
    }
	return 0;
}

void merge(int a[], int l1, int r1, int l2, int r2)
{
    int i = l1, j = l2;
    int temp[100] = {0};  // 临时数组 
    int index = 0;
    /* 两个数组同时遍历, 一个遍历完则停止 */ 
    for (; i<=r1 && j<=r2;)
    {
        if (a[i]<a[j])
            temp[index++] = a[i++];
        else
            temp[index++] = a[j++];
    }
    /* 两个数组不等长则输出剩余元素(必定有序) */ 
    while(i<=r1) temp[index++] = a[i++];
    while(j<=r2) temp[index++] = a[j++];
    /* 将结果赋回原数组 */ 
    for (int i=0; i<index; i++)
        a[l1+i] = temp[i];
}

void sort_merge(int a[], int left, int right)
{
    if (left<right)  // 递归到被拆分数组只有一个元素时停止
    {
        int mid = (left + right) / 2;  // 从中间拆分数组 
        /* 先算完左半边, 再算右半边 */ 
        sort_merge(a, left, mid);    // 对左半边数组递归 
        sort_merge(a, mid+1, right);  // 对右半边数组递归 
        merge(a, left, mid, mid+1, right);  // 有序归并两个数组 
    }
}
```

#### 循环版

```c++
#include <iostream>
#include <algorithm>
using namespace std;

void merge(int a[], int l1, int r1, int l2, int r2);

int main(void)
{
	int a[5] = {5,2,4,1,3};
	int len = sizeof(a) / 4;
	for (int i=0; i<len; i++)
	{
	    printf("%d ", a[i]);
    }
	printf("\n");
	/* step相当于归并的数组大小, 从2开始, 2的指数增长 */
	/* step/2<len 指必须要有一组数组完全位于总数组内,并且至少还要留给第二步1个元素(不取等号) */
	/* 例如step增长到4时, 分组为{1,2,3,4},{5}, 符合要求但不能继续增长 */ 
	for (int step=2; step/2<len; step*=2)
	{
	    /* 对每个子组归并 */ 
	    for (int i=0; i<=len; i+=step)
	    {
	        /* 当前步子一分为二, 左右归并 */
	        int mid = i + step / 2 - 1;
	        /* 注意判断不要越界 */
	        merge(a,i, mid, mid+1, min(i+step, len));  // sort() 前闭后开 
        }
    }
	
	for (int i=0; i<len; i++)
	{
	    printf("%d ", a[i]);
    }
	return 0;
}

void merge(int a[], int l1, int r1, int l2, int r2)
{
    int i = l1, j = l2;
    int temp[100] = {0};  // 临时数组 
    int index = 0;
    /* 两个数组同时遍历, 一个遍历完则停止 */ 
    for (; i<=r1 && j<=r2;)
    {
        if (a[i]<a[j])
            temp[index++] = a[i++];
        else
            temp[index++] = a[j++];
    }
    /* 两个数组不等长则输出剩余元素(必定有序) */ 
    while(i<=r1) temp[index++] = a[i++];
    while(j<=r2) temp[index++] = a[j++];
    /* 将结果赋回原数组 */ 
    for (int i=0; i<index; i++)
        a[l1+i] = temp[i];
}
```

#### 循环模拟版

```c++
#include <iostream>
#include <algorithm>
using namespace std;

int main(void)
{
	int a[5] = {5,2,4,1,3};
	int len = sizeof(a) / 4;
	for (int i=0; i<len; i++)
	{
	    printf("%d ", a[i]);
    }
	printf("\n");
	/* step相当于归并的数组大小, 从2开始, 2的指数增长 */
	/* step/2<len 指必须要有一组数组完全位于总数组内,并且至少还要留给第二步1个元素(不取等号) */
	/* 例如step增长到4时, 分组为{1,2,3,4},{5}, 符合要求但不能继续增长 */ 
	for (int step=2; step/2<len; step*=2)
	{
	    /* 对每个子组排序, 相当于进行一次下级归并结果 */ 
	    for (int i=0; i<=len; i+=step)
	    { 
	        /* 注意判断不要越界 */
	        if (i+step-1<=len-1)
	           sort(a+i, a+i+step);  // sort() 前闭后开 
	        else sort(a+i, a+len);
        }
    }
	
	for (int i=0; i<len; i++)
	{
	    printf("%d ", a[i]);
    }
	return 0;
}
```

### 快速排序

[[3-计算机科学/0-数据结构与算法/快速排序|快速排序]]

## sort()

### cmp() 函数构造

```c++
bool cmp(a,b)
{
    return a>b; // 降序
    return a<b  // 升序
}
```

可以使用 `else if` 实现多条件排序.

## 贪心算法

## two pointers

有序序列的两层循环, 可以想办法变成左右两个指针的移动, 减小时间复杂度.

