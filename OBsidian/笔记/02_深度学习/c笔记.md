# ***c++笔记***

## 1.前期

#### 1.头文件的区别

c 和 c++ 在格式上的区别

```c++
# include<iostream>
using namespace std;
//c++

# include<stdio.h>
//c
```



#### 2.基本格式

```c++
#include <iostream>
using namespace std;

int main()
{

    ***
        
    system("pause");
    return 0;
}
```



#### *3.前置递增和后置递增的区别：*

```c++
//前置递增 先让变量 +1 然后再进行表达式的运算

int a2 = 10;
int b2 = ++ a2 * 10;
cout << "a2 = "<< a2 << endl;
cout << "ab2 = "<< b2 << endl;

/*输出:
a2 =11    b2 =110
*/

/后置递增 先进行表达式的运算 再进行+1
int a3 = 10;
int b3 = a3 ++ * 10;
cout << "a3 = "<< a3 << endl;
cout << "b3 = "<< b3 << endl;

/*输出:
a3 = 11   b3 = 100
*/
```



#### 4.水仙花数案例

```c++
#include <iostream>
using namespace std;

int main()
{
    int k = 0, j = 100, n1, n2, n3;

    for (int i = 100; i < 1000; i++)
    {
        n1 = i / 100;
        n2 = (i / 10) % 10;
        n3 =  i % 10;
        //cout << n1 << endl;
        //cout << n2 << endl;
        //cout << n3 << endl; // 测试数值
        if (((n1*n1*n1) + (n2*n2*n2) + (n3*n3*n3)) == i)
        {
            cout << i << endl;
        }

    }
    system("pause");
    return 0;
}
```



#### 5.“go to”代码

```c++
A
goto FLAG;
B
C
FLAG;
D
//执行：A D
```



#### 6.冒泡法进行数组排序：

```c++
int main()
{
    int a[5] = {300,350,200,400,250 };
    int b = 0;

    for (int i = 0; i < 5; i++)
    {
        if (a[i] > b) 
    //轮流和数组进行比较替换最大值
            
        {
            b = a[i];
        }
    }
    cout << b << endl;
    system("pause");
    return 0;
}
```



#### 7.函数的分文件书写

1.创建后缀名为.h的头文件

```c++
//swap.h文件
#include<iostream>
using namespace std;

//声明
void swap(int a , int b)
```

2.创建后缀名为.cpp的源文件

```c++
//swap.cpp文件
#include "swap.h"

//然后定义函数
```

3.在头文件中写函数的声明

4.在源文件中写函数的定义



#### 8.值传递

**形参无法改变实参**

## 2.指针

#### 1.空指针

用途主要是初始化指针变量

但是 **重要！!** 空指针指向的内存是不可以进行访问的！

示例：

```c++
int main(){
	int * p = NULL; //注意要大写 NULL
}
```

#### 2.野指针

指针变量指向非法的内存空间

示例：

```c++
int main(){
	//野指针
	int * p = 0x1100;
	
	cout<< *p <<endl;
	//报错 读取访问异常 权限冲突
}
```

<u>*此地址不属于系统为程序分配的内存空间*</u>

#### 3.const修饰指针变量

*const修饰指针有三种情况*

 *1.const修饰指针  常量指针*

 *2.const修饰常量  指针常量*

 *3.const既修饰指针，又修饰常量*

示例：

```c++
int main(){
    int a = 10;
    int b = 10;
    
    //情况一: const修饰的是指针 指针的指向可以改 但是指针指向的值不能改变
    const int * p1 = &a ;
    p1 = &b ; //正确 
    *p1 = 100 //错误
        
	//情况二：const修饰的是常量 指针指向不可以改 但是指针指针指向的值可以改变
	int * const p2 = &a ;
    p2 = &b; //错误
    *p2 = b；//正确
        
	//情况三：const既修饰指针也修饰变量 则两个值都不可以改变
    const int * const p3 = &a ;
    p3 = &b; //错误
    *p3 = &b;//错误
    
    system("pause");
    
   return 0;
}
```

#### 4.指针和函数：

正常情况下函数中形参无法改变实参 见1.8

但是使用了指针之后函数就可以通过改变地址对应的值的方式 改变实参的值

```c++
//地址传递:
//创建交换函数：
void swap(int * p1 , int * p2)
{
    int temp = * p1;
    *p1 = *p2;
    *p2 = temp;
}
//主函数可以进行验证
int main(){
    int a = 10;
    int b = 20;
    
    swap(&a,&b);
    cout<<"a = "<<a<<endl;
    cout<<"b = "<<b<<endl;
    //输出结果：
    a = 20;
    b = 10;
    //地址传递会改变实参！
}

```

![image-20240921131337123](C:\Users\Slexy\AppData\Roaming\Typora\typora-user-images\image-20240921131337123.png)

#### 5.指针、函数、数组的结合

***<u>升序排列案例</u>***：

```c++
#include <iostream>
using namespace std;

void arr(int *p, int c)  //建立排序函数
{
    cout << "c=" << c << endl;
    int t;
    for (int i = 0; i < c-1; i++)
    {
        for (int j = 0; j < c - 1 - i; j++)
        {
            if ( p[j] > p[j + 1] ) 
            {
                t = p[j];
                p[j] = p[j + 1];
                p[j + 1] = t;
            }
        }
    }
}    
//建立排序函数

void printf(int* arr, int c)
{
    for (int i = 0; i < c; i++)
    {
        cout << arr[i] <<endl;
    }
}
//建立输出函数


int main()
{
    int a[10] = {10,5,3,2,1,4,6,8,9,7}; //创建数组
    
    int c = sizeof(a) / sizeof(a[0]);//得出数组的长度

    arr(a, c);

    printf(a, c);

    system("pause");
    return 0;
}
```



## 3.结构体

#### 1.结构体定义和使用

**语法：**`struct 结构体名 { 结构体成员列表 }；`

通过结构体创建变量的方式有三种：

* struct 结构体名.变量名
* struct 结构体名.变量名 = { 成员1值 ， 成员2值...}
* 定义结构体时顺便创建变量

**！重点！**  ***<u>结构体不能放在main函数里面需要另外单列</u>***

示例：

```c++
//创建结构体
struct student
{
    //成员列表
    
    //姓名
    string name;
    //年龄
    int age;
    //分数
    int score;

}；
    //通过学生类型创建学生
   int main()
{
    //1
    struct student s1;
    s1.name = "张三";
    s1.score = 100;
    s1.age = 18 ;
    
    //2
    struct student s2 = {"李四",19,80};
    
    //3
    //定义结构体时顺便创建变量
    
}
```



#### 2.结构体数组

**作用：**将自定义的结构体放入到数组中方便维护

**语法：**` struct  结构体名 数组名[元素个数] = {  {} , {} , ... {} }`

**示例：**

**示例：**

```c++
//结构体定义
struct student
{
	//成员列表
	string name;  //姓名
	int age;      //年龄
	int score;    //分数
}

int main() 
	{
	
	//结构体数组
	struct student arr[3]=
	{
		{"张三",18,80 },
		{"李四",19,60 },
		{"王五",20,70 }
	};

	for (int i = 0; i < 3; i++)
	{
		cout << "姓名：" << arr[i].name << " 年龄：" << arr[i].age << " 分数：" << arr[i].score << endl;
	}

	system("pause");

	return 0;
}
```



#### 3.结构体指针

作用：通过指针访问结构体中的成员



- 利用操作符 `-> `可以通过结构体指针访问结构体属性
- 利用（*p）也可以通过结构体指针访问结构体属性

**示例：**

```c++
//结构体定义
struct student
{
	string name;  //姓名
	int age;      //年龄
	int score;    //分数
};


int main() {
	
	struct student stu = { "张三",18,100, };
	
	struct student * p = &stu;
	
	p->score = 80; //指针通过 -> 操作符可以访问成员

	cout << "姓名：" << p->name << " 年龄：" << p->age << " 分数：" << p->score << endl;
	
	system("pause");

	return 0;
}
```



#### 4.结构体嵌套结构体

**作用：**结构体中的成员可以是另外一个结构体

**示例：**

```c++
//学生结构体定义
struct student
{
	//成员列表
	string name;  //姓名
	int age;      //年龄
	int score;    //分数
};

//教师结构体定义
struct teacher
{
    //成员列表
	int id; //职工编号
	string name;  //教师姓名
	int age;   //教师年龄
	struct student stu; //子结构体 学生
};


int main() {

	struct teacher t1;
	t1.id = 10000;
	t1.name = "老王";
	t1.age = 40;

	t1.stu.name = "张三";
	t1.stu.age = 18;
	t1.stu.score = 100;

	cout << "教师 职工编号： " << t1.id << " 姓名： " << t1.name << " 年龄： " << t1.age << endl;
	
	cout << "辅导学员 姓名： " << t1.stu.name << " 年龄：" << t1.stu.age << " 考试分数： " << t1.stu.score << endl;

	system("pause");

	return 0;
}
```



*<u>可以通过`a.b.c`的方式访问结构体中的结构体和 其他单位</u>*



#### 5.结构体做函数参数

传递方式有两种：

1. 值传递
2. 地址传递

**示例：**

```c++
//学生结构体定义
struct student
{
	//成员列表
	string name;  //姓名
	int age;      //年龄
	int score;    //分数
};

//值传递
void printStudent(student stu )
{
	stu.age = 28;
	cout << "子函数中 姓名：" << stu.name << " 年龄： " << stu.age  << " 分数：" << stu.score << endl;
}

//地址传递
void printStudent2(student *stu)
{
	stu->age = 28;
	cout << "子函数中 姓名：" << stu->name << " 年龄： " << stu->age  << " 分数：" << stu->score << endl;
}

int main() {

	student stu = { "张三",18,100};
	//值传递
	printStudent(stu);
	cout << "主函数中 姓名：" << stu.name << " 年龄： " << stu.age << " 分数：" << stu.score << endl;

	cout << endl;

	//地址传递
	printStudent2(&stu);
	cout << "主函数中 姓名：" << stu.name << " 年龄： " << stu.age  << " 分数：" << stu.score << endl;

	system("pause");

	return 0;
}
```



***<u>(但是注意值传递同样无法修改数据 并且值传递会传递整个的数据 当结构体非常大时 浪费了很多的内存和空间 故一般使用地址传递)</u>***



#### 6.结构体案例

**案例描述：**

学校正在做毕设项目，每名老师带领5个学生，总共有3名老师，需求如下

设计学生和老师的结构体，其中在老师的结构体中，有老师姓名和一个存放5名学生的数组作为成员

学生的成员有姓名、考试分数，创建数组存放3名老师，通过函数给每个老师及所带的学生赋值

最终打印出老师数据以及老师所带的学生数据。



**示例：**

```c++
#include <iostream>
using namespace std;
#include <string>

//创建学生结构体
struct student
{
    //列表
    string sname;
    int score;
};   
//创建教师结构体
struct teacher
{
    string tname;
    student a[5];
};   
//输入学生&教师数据 函数
void a(struct teacher abc[] , int len )
{
    string b = "ABCDE";
    for (int i = 0; i < len; i++)
    {
        abc[i].tname = "teacher_";
        abc[i].tname += b[i];
        for (int j = 0; j < 5; j++)
        {
            abc[i].a[j].sname = "student_";
            abc[i].a[j].sname += b[j];
            int random = rand() % 100;
            abc[i].a[j].score = random;
        }        
    }
}
//输出学生&教师数据 函数
void printf(teacher abc[], int a)
{
    for (int i = 0; i < a; i++)
    {
        cout << "老师的姓名是:" << abc[i].tname << endl;
        for (int j = 0; j < 5; j++)
        {
            cout << "\t学生的姓名是：" << abc[i].a[j].sname << "分数为"
                << abc[i].a[j].score<<endl;

        }
    }
}

int main()
{
     //1.创建老师 同学结构体 （数组）
     struct teacher abc[3];
     //2.创建函数 输入 老师 & 学生的个人信息
     a(abc, 3);
     //3.输出
     printf(abc, 3);

     system("pause");
     return 0;
}
```



## 4.案例

通讯录管理系统案例：

**要求：**
通讯录是一个可以记录亲人、好友信息的工具

系统中需要实现的功能如下:

1. 添加联系人:向通讯录中添加新人，信息包括(姓名、年龄、联系电话)最多记录100人
2. 显示联系人:显示通讯录中所有联系人信息
3. 删除联系人:按照姓名进行删除指定联系人
4. 查找联系人:按照姓名查看指定联系人信息
5. 修改联系人:按照姓名重新修改指定联系人
6. 清空联系人:清空通讯录中所有信息
7. 退出通讯录:退出当前使用的通讯录



*<u>**示例：**</u>*

```c++
#define _CRT_SECURE_NO_WARNINGS

#include<iostream>
#include<string>
using namespace std;

//创建联系人结构体
struct man
{
	//联系人姓名
	string name;

	//联系人电话
	string tel;

	//联系人年龄
	string age;

	//记录结构体中存储的联系人数量
	int size = 0;

};

//创建添加联系人函数
void add(man* arr)
{
	cout << "请输入姓名：" << endl;
	cin >> arr[arr->size].name;

	cout << "请输入年龄：" << endl;
	cin >> arr[arr->size].age;

	cout << "请输入电话号码：" << endl;
	cin >> arr[arr->size].tel;

	arr->size++;
	system("pause");
	system("cls");
	
}

//创建显示联系人函数
void show(man* arr)
{
	if (arr->size==0)
	{
		cout << "没人呢" << endl;
	}
	else
	{
		for (int i = 0; i < arr->size; i++)
		{
			cout << "姓名：" << arr[i].name << "\t"
				<< "年龄：" << arr[i].age << "\t"
				<< "电话号：" << arr[i].tel << endl;
		}
	}
	
	system("pause");
	system("cls");
}

//查找联系人所在的位置
int intserch(man* arr)
{
	string temp;
	cin >> temp;
	for (int i = 0; i < arr->size; i++)
	{
		//cout << arr->size;
		if (temp == arr[i].name)
		{
			return i;
		}
	}
	return -1;
}

//查找联系人
void serch(man* arr)
{	
	int a;
	cout << "请输入查找的联系人名字" << endl;	
	a = intserch(arr);

	if (a == -1)
	{
		cout << "查无此人" << endl;
		system("pause");
		system("cls");
	}
	else
	{
		cout << "姓名：" << arr[a].name << "\t"
			<< "年龄：" << arr[a].age << "\t"
			<< "电话号：" << arr[a].tel << endl;
		system("pause");
		system("cls");
	}



}

//删除联系人
void del(man* arr)
{
	cout << "请输入你要删除的联系人的名字:" << endl;
	int b = intserch(arr);

	if (b == -1)
	{
		cout << "查无此人" << endl;
	}
	else
	{
		for (int i = b; i < arr->size - 1; i++)
		{
			arr[i] = arr[i + 1];
		}
	}
	arr->size--;
	system("pause");
	system("cls");
}

//修改联系人
void reinput(man* arr)
{
	cout << "请输入你要修改的联系人的名字:" << endl;
	int a = intserch(arr);
	if (a==-1)
	{
		cout << "查无此人" << endl;
	}
	else
	{
		cout << "原信息：" << endl;
		cout << "姓名：" << arr[a].name << "\t"
			 << "年龄：" << arr[a].age << "\t"
			 << "电话号：" << arr[a].tel << endl;
		//修改
		cout << "请输入新的姓名：" << endl;
		cin >> arr[a].name;

		cout << "请输入新的年龄：" << endl;
		cin >> arr[a].age;

		cout << "请输入新的电话号码：" << endl;
		cin >> arr[a].tel;
	}
	system("pause");
	system("cls");
}

//清空联系人
void alldel(man* arr)
{
	arr->size = 0;
	cout << "清理完毕 期待您的下一次使用" << endl;
	system("pause");
	system("cls");
}

//主函数 实现通讯录管理功能
int main(void)
{
	man arry[100];

	while (true)
	{
		cout << "****************************" << endl;
		cout << "****** 1、添加联系人 *******" << endl;
		cout << "****** 2、显示联系人 *******" << endl;
		cout << "****** 3、删除联系人 *******" << endl;
		cout << "****** 4、查找联系人 *******" << endl;
		cout << "****** 5、修改联系人 *******" << endl;
		cout << "****** 6、清空联系人 *******" << endl;
		cout << "****** 0、退出联系人 *******" << endl;
		cout << "****************************" << endl;
		cout << "----------------------------" << endl;
		cout << endl;
		int a;
		cin >> a;

		switch (a)
		{
		//添加联系人
		case 1:
			add(arry);
			break;
		//显示联系人
		case 2:
			show(arry);
			break;
		//删除联系人
		case 3:
			del(arry);
			break;
		//查找联系人
		case 4:
			serch(arry);
			break;
		//修改联系人
		case 5:
			reinput(arry);
			break;
		case 6:
		//清除通讯录
			alldel(arry);
			break;
		//退出程序
		case 0:
			cout << "感谢您的使用，下次再见" << endl;
			system("pause");
			return 0;
		//循环
		default:
			cout << "输入错误 未找到该功能" << endl;
			system("pause");
			break;
		}
		system("cls");
	}
	system("pause");
	return 0;
}

```





## 5.c++中的引用

#### 1.引用的基本语法

引用基本语法为

`数据类型 + &变量名 = 原变量名`

示例：

```c++
int a = 10;
int &b = a;
//则b = a = 10
```



#### 2 引用注意事项

* 引用必须初始化
* 引用在初始化后，不可以改变

示例：

```C++
int main() {

	int a = 10;
	int b = 20;
	//int &c; //错误，引用必须初始化
	int &c = a; //一旦初始化后，就不可以更改
	c = b; //这是赋值操作，不是更改引用

	cout << "a = " << a << endl;
	cout << "b = " << b << endl;
	cout << "c = " << c << endl;

	system("pause");

	return 0;
}
```



#### 3 引用做函数参数

**作用：**函数传参时，可以利用引用的技术让形参修饰实参

**优点：**可以简化指针修改实参



**示例：**

```C++


// 引用传递
void mySwap03(int& a, int& b) {
	int temp = a;
	a = b;
	b = temp;
}

int main() {

	int a = 10;
	int b = 20;

	mySwap01(a, b);
	cout << "a:" << a << " b:" << b << endl;

	mySwap02(&a, &b);
	cout << "a:" << a << " b:" << b << endl;

	mySwap03(a, b);
	cout << "a:" << a << " b:" << b << endl;

	system("pause");

	return 0;
}

```



#### 4 引用做函数返回值



作用：引用是可以作为函数的返回值存在的

注意：**不要返回局部变量引用**

用法：函数调用作为左值



**示例：**

```C++
//返回局部变量引用
int& test01() {
	int a = 10; //局部变量
	return a;
}

//返回静态变量引用
int& test02() {
	static int a = 20;
	return a;
}

int main() {

	//不能返回局部变量的引用
	int& ref = test01();
	cout << "ref = " << ref << endl;
	cout << "ref = " << ref << endl;

	//如果函数做左值，那么必须返回引用
	int& ref2 = test02();
	cout << "ref2 = " << ref2 << endl;
	cout << "ref2 = " << ref2 << endl;

	test02() = 1000;

	cout << "ref2 = " << ref2 << endl;
	cout << "ref2 = " << ref2 << endl;

	system("pause");

	return 0;
}
```





#### 5 引用的本质

本质：**引用的本质在c++内部实现是一个指针常量.**

```C++
//发现是引用，转换为 int* const ref = &a;
void func(int& ref){
	ref = 100; // ref是引用，转换为*ref = 100
}
int main(){
	int a = 10;
    
    //自动转换为 int* const ref = &a; 指针常量是指针指向不可改，也说明为什么引用不可更改
	int& ref = a; 
	ref = 20; //内部发现ref是引用，自动帮我们转换为: *ref = 20;
    
	cout << "a:" << a << endl;
	cout << "ref:" << ref << endl;
    
	func(a);
	return 0;
}
```





#### 6 常量引用



**作用：**常量引用主要用来修饰形参，防止误操 在函数形参列表中，可以加==const修饰形参==，防止形参改变实参

**示例：**



```C++
//引用使用的场景，通常用来修饰形参
void showValue(const int& v) {
	//v += 10;
	cout << v << endl;
}

int main() {

	//int& ref = 10;  引用本身需要一个合法的内存空间，因此这行错误
	//加入const就可以了，编译器优化代码，int temp = 10; const int& ref = temp;
	const int& ref = 10;

	//ref = 100;  //加入const后不可以修改变量
	cout << ref << endl;

	//函数中利用常量引用防止误操作修改实参
	int a = 10;
	showValue(a);

	system("pause");

	return 0;
}
```





## 3 函数提高

#### 1 函数默认参数



在C++中，函数的形参列表中的形参是可以有默认值的。

语法：` 返回值类型  函数名 （参数= 默认值）{}`



**示例：**

```C++
int func(int a, int b = 10, int c = 10) {
	return a + b + c;
}

//1. 如果某个位置参数有默认值，那么从这个位置往后，从左向右，必须都要有默认值
//2. 如果函数声明有默认值，函数实现的时候就不能有默认参数
int func2(int a = 10, int b = 10);
int func2(int a, int b) {
	return a + b;
}

int main() {

	cout << "ret = " << func(20, 20) << endl;
	cout << "ret = " << func(100) << endl;

	system("pause");

	return 0;
}
```







#### 2 函数占位参数



C++中函数的形参列表里可以有占位参数，用来做占位，调用函数时必须填补该位置



**语法：** `返回值类型 函数名 (数据类型){}`



**示例：**

```C++
//函数占位参数 ，占位参数也可以有默认参数
void func(int a, int) {
	cout << "this is func" << endl;
}

int main() {

	func(10,10); //占位参数必须填补

	system("pause");

	return 0;
}
```









#### 3 函数重载

**作用：**函数名可以相同，提高复用性

**函数重载满足条件：**

* 同一个作用域下
* 函数名称相同
* 函数参数**类型不同**  或者 **个数不同** 或者 **顺序不同**



**注意:**  函数的返回值不可以作为函数重载的条件



**示例：**

```C++
//函数重载需要函数都在同一个作用域下
void func()
{
	cout << "func 的调用！" << endl;
}
void func(int a)
{
	cout << "func (int a) 的调用！" << endl;
}
void func(double a)
{
	cout << "func (double a)的调用！" << endl;
}
void func(int a ,double b)
{
	cout << "func (int a ,double b) 的调用！" << endl;
}
void func(double a ,int b)
{
	cout << "func (double a ,int b)的调用！" << endl;
}

//函数返回值不可以作为函数重载条件
//int func(double a, int b)
//{
//	cout << "func (double a ,int b)的调用！" << endl;
//}


int main() {

	func();
	func(10);
	func(3.14);
	func(10,3.14);
	func(3.14 , 10);
	
	system("pause");

	return 0;
}
```



**注意事项**

* 引用作为重载条件
* 函数重载碰到函数默认参数



**示例：**

```C++
//函数重载注意事项
//1、引用作为重载条件

void func(int &a)
{
	cout << "func (int &a) 调用 " << endl;
}

void func(const int &a)
{
	cout << "func (const int &a) 调用 " << endl;
}


//2、函数重载碰到函数默认参数

void func2(int a, int b = 10)
{
	cout << "func2(int a, int b = 10) 调用" << endl;
}

void func2(int a)
{
	cout << "func2(int a) 调用" << endl;
}

int main() {
	
	int a = 10;
	func(a); //调用无const
	func(10);//调用有const


	//func2(10); //碰到默认参数产生歧义，需要避免

	system("pause");

	return 0;
}
```





## 4.类和对象

c++面向对象的三大特性为：封装、继承、多态



c++的对象上有 属性和行为

#### 1.封装的意义：

**语法：** `class 类名{   访问权限： 属性  / 行为  };`

**示例代码：**



```c++
//圆周率
const double PI = 3.14;

//1、封装的意义
//将属性和行为作为一个整体，用来表现生活中的事物

//封装一个圆类，求圆的周长
//class代表设计一个类，后面跟着的是类名
class Circle
{
public:  //访问权限  公共的权限

	//属性
	int m_r;//半径

	//行为
	//获取到圆的周长
	double calculateZC()
	{
		//2 * pi  * r
		//获取圆的周长
		return  2 * PI * m_r;
	}
};

int main() {

	//通过圆类，创建圆的对象
	// c1就是一个具体的圆
	Circle c1;
	c1.m_r = 10; //给圆对象的半径 进行赋值操作

	//2 * pi * 10 = = 62.8
	cout << "圆的周长为： " << c1.calculateZC() << endl;

	system("pause");

	return 0;
}
```

#### 2 struct和class区别



在C++中 struct和class唯一的**区别**就在于 **默认的访问权限不同**

区别：

* struct 默认权限为公共
* class   默认权限为私有



三种权限分别是 ：

1. public 型        公有
2. private型       私有
3. protect型       私有



```C++
class C1
{
	int  m_A; //默认是私有权限
};

struct C2
{
	int m_A;  //默认是公共权限
};

int main() {

	C1 c1;
	c1.m_A = 10; //错误，访问权限是私有

	C2 c2;
	c2.m_A = 10; //正确，访问权限是公共

	system("pause");

	return 0;
}
```





#### 3 成员属性设置为私有



**优点1：**将所有成员属性设置为私有，可以自己控制读写权限

**优点2：**对于写权限，我们可以检测数据的有效性



**示例：**

```C++
class Person {
public:

	//姓名设置可读可写
	void setName(string name) {
		m_Name = name;
	}
	string getName()
	{
		return m_Name;
	}


	//获取年龄 
	int getAge() {
		return m_Age;
	}
	//设置年龄
	void setAge(int age) {
		if (age < 0 || age > 150) {
			cout << "你个老妖精!" << endl;
			return;
		}
		m_Age = age;
	}

	//情人设置为只写
	void setLover(string lover) {
		m_Lover = lover;
	}

private:
	string m_Name; //可读可写  姓名
	
	int m_Age; //只读  年龄

	string m_Lover; //只写  情人
};


int main() {

	Person p;
	//姓名设置
	p.setName("张三");
	cout << "姓名： " << p.getName() << endl;

	//年龄设置
	p.setAge(50);
	cout << "年龄： " << p.getAge() << endl;

	//情人设置
	p.setLover("苍井");
	//cout << "情人： " << p.m_Lover << endl;  //只写属性，不可以读取

	system("pause");

	return 0;
}
```



#### 4 圆判断点的位置案例



**示例：**

```c++
#define _CRT_SECURE_NO_WARNINGS
#include<iostream>
using namespace std;

class point {
public:
	void getx(int i) {
		x = i;
	}
	int returnx() {
		return x;
	}
	void gety(int j) {
		x = j;
	}
	int returny() {     
		return y;
	}

private:
	int x;
	int y;
};

class circle
{
public:
	void getr(int j) {
		c_r = j;
	}
	int returnr() {
		return c_r;
	}
	void getcentral(point a) {
		central = a;
	}
	point returncentral() {
		return central;
	}

private:
	int c_r;
	point central;
};

void panduan(circle& c, point& p) {
	int a = (c.returncentral().returnx() - p.returnx())
		*   (c.returncentral().returnx() - p.returnx());
	int b = (c.returncentral().returny() - p.returny())
		*   (c.returncentral().returny() - p.returny());
	if (a + b == c.returnr())
	{
		cout<<"在圆上"<<endl;
	}
	else if (a + b <= c.returnr())
	{
		cout << "在圆内" << endl;
	}
	else if (a + b >= c.returnr())
	{
		cout << "在圆外" << endl;
	}
}


int main() {
	while (true)
	{


		circle c;
		point p;
		point p1;
		int a, b, d;
		cout << "请输入圆的半径" << endl;
		cin >> a;

		p.getx(0);
		p.gety(0);
		c.getr(a);
		c.getcentral(p);

		cout << "请输入点的x坐标：" << endl;
		cin >> b;
		p1.getx(b);
		cout << "请输入点的y坐标：" << endl;
		cin >> d;
		p1.gety(d);

		panduan(c, p1); 
		
		system("pause");
		system("cls");
	}
	
	return 0;
}
```



#### 5.构造函数与析构函数：

**构造函数语法：**`类名(){}`

1. 构造函数，没有返回值也不写void
2. 函数名称与类名相同
3. 构造函数可以有参数，因此可以发生重载
4. 程序在调用对象时候会自动调用构造，无须手动调用,而且只会调用一次



**析构函数语法：** `~类名(){}`

1. 析构函数，没有返回值也不写void
2. 函数名称与类名相同,在名称前加上符号  ~
3. 析构函数不可以有参数，因此不可以发生重载
4. 程序在对象销毁前会自动调用析构，无须手动调用,而且只会调用一次



示例：

```c++
#define _CRT_SECURE_NO_WARNINGS

#include<iostream>
using namespace std;

class phone
{
public:
	phone(string name) : p_name(name)
	{
	}
	string p_name;
};

//当其他类的对象在父类里面时，先构造父类里面的对象再构造父类本身
class man
{
public:
	man(int age1, string name) :p_name(name), age(age1)
	{
	}
	int age;
	phone p_name;
};
//同样的析构的时候先析构自己再析构其他的对象



int main()
{
	man m1(18, "华为");
	cout << "年龄是：" << m1.age << endl;
	cout << "用的手机是：" << m1.p_name.p_name << endl;
	system("pause");
	return 0;
}
```



#### 6.构造函数的分类及调用

两种分类方式：

​	按参数分为： 有参构造和无参构造

​	按类型分为： 普通构造和拷贝构造

三种调用方式：

​	括号法

​	显示法

​	隐式转换法



示例：

```c++
#define _CRT_SECURE_NO_WARNINGS
#include<iostream>
using namespace std;

//class Person {
//
//public:
//	Person() {
//		cout << "构造函数调用1" << endl;
//	}
//	Person(int a) {
//		cout << "构造函数调用2" << endl;
//	}
//	~Person() {
//		cout << "构析函数调用1" << endl;
//	}
//	Person(const Person &p) {
//		cout << "拷贝函数的调用" << endl;
//
//	}
//};


//调用函数
//void a() {
//	Person p1;
//	Person p2(p1);
//}



class a {
public:
	void c(int b) 
	{
		p = new int(b);
	}
	int *p;
};

int main() {
	a a1;
	a1.c(10);
	cout << *(a1.p) << endl;
	
	system("pause");
	return 0;
}
```



#### 7.构造函数调用规则

默认情况下，c++编译器至少给一个类添加3个函数

1．默认构造函数(无参，函数体为空)

2．默认析构函数(无参，函数体为空)

3．默认拷贝构造函数，对属性进行值拷贝



构造函数调用规则如下：

* 如果用户定义有参构造函数，c++不在提供默认无参构造，但是会提供默认拷贝构造


* 如果用户定义拷贝构造函数，c++不会再提供其他构造函数



示例：

```C++
class Person {
public:
	//无参（默认）构造函数
	Person() {
		cout << "无参构造函数!" << endl;
	}
	//有参构造函数
	Person(int a) {
		age = a;
		cout << "有参构造函数!" << endl;
	}
	//拷贝构造函数
	Person(const Person& p) {
		age = p.age;
		cout << "拷贝构造函数!" << endl;
	}
	//析构函数
	~Person() {
		cout << "析构函数!" << endl;
	}
public:
	int age;
};

void test01()
{
	Person p1(18);
	//如果不写拷贝构造，编译器会自动添加拷贝构造，并且做浅拷贝操作
	Person p2(p1);

	cout << "p2的年龄为： " << p2.age << endl;
}

void test02()
{
	//如果用户提供有参构造，编译器不会提供默认构造，会提供拷贝构造
	Person p1; //此时如果用户自己没有提供默认构造，会出错
	Person p2(10); //用户提供的有参
	Person p3(p2); //此时如果用户没有提供拷贝构造，编译器会提供

	//如果用户提供拷贝构造，编译器不会提供其他构造函数
	Person p4; //此时如果用户自己没有提供默认构造，会出错
	Person p5(10); //此时如果用户自己没有提供有参，会出错
	Person p6(p5); //用户自己提供拷贝构造
}

int main() {

	test01();

	system("pause");

	return 0;
}
```



#### 8.深拷贝与浅拷贝



**示例：**

```C++
class Person {
public:
	//无参（默认）构造函数
	Person() {
		cout << "无参构造函数!" << endl;
	}
	//有参构造函数
	Person(int age ,int height) {
		
		cout << "有参构造函数!" << endl;

		m_age = age;
		m_height = new int(height);
		
	}
	//拷贝构造函数  
	Person(const Person& p) {
		cout << "拷贝构造函数!" << endl;
		//如果不利用深拷贝在堆区创建新内存，会导致浅拷贝带来的重复释放堆区问题
		m_age = p.m_age;
		m_height = new int(*p.m_height);
		
	}

	//析构函数
	~Person() {
		cout << "析构函数!" << endl;
		if (m_height != NULL)
		{
			delete m_height;
		}
	}
public:
	int m_age;
	int* m_height;
};

void test01()
{
	Person p1(18, 180);

	Person p2(p1);

	cout << "p1的年龄： " << p1.m_age << " 身高： " << *p1.m_height << endl;

	cout << "p2的年龄： " << p2.m_age << " 身高： " << *p2.m_height << endl;
}

int main() {

	test01();

	system("pause");

	return 0;
}
```

> 如果属性有在堆区开辟的，一定要自己提供拷贝构造函数，防止浅拷贝带来的问题



#### 9.初始化列表

**语法：**`构造函数()：属性1(值1),属性2（值2）... {}`



**示例：**

```C++
class Person {
public:

	////传统方式初始化
	//Person(int a, int b, int c) {
	//	m_A = a;
	//	m_B = b;
	//	m_C = c;
	//}

	//初始化列表方式初始化
	Person(int a, int b, int c) :m_A(a), m_B(b), m_C(c) {}
	void PrintPerson() {
		cout << "mA:" << m_A << endl;
		cout << "mB:" << m_B << endl;
		cout << "mC:" << m_C << endl;
	}
private:
	int m_A;
	int m_B;
	int m_C;
};

int main() {

	Person p(1, 2, 3);
	p.PrintPerson();


	system("pause");

	return 0;
}
```



#### 10.静态成员

静态成员就是在成员变量和成员函数前加上关键字static，称为静态成员

静态成员分为：

1.静态成员变量

*  所有对象共享同一份数据
*  在编译阶段分配内存
*  类内声明，类外初始化

2.静态成员函数

*  所有对象共享同一个函数
*  静态成员函数只能访问静态成员变量



**示例：**

```C++
class Person
{
	
public:

	static int m_A; //静态成员变量

	//静态成员变量特点：
	//1 在编译阶段分配内存
	//2 类内声明，类外初始化
	//3 所有对象共享同一份数据

private:
	static int m_B; //静态成员变量也是有访问权限的
};
int Person::m_A = 10;
int Person::m_B = 10;

void test01()
{
	//静态成员变量两种访问方式

	//1、通过对象
	Person p1;
	p1.m_A = 100;
	cout << "p1.m_A = " << p1.m_A << endl;

	Person p2;
	p2.m_A = 200;
	cout << "p1.m_A = " << p1.m_A << endl; //共享同一份数据
	cout << "p2.m_A = " << p2.m_A << endl;

	//2、通过类名
	cout << "m_A = " << Person::m_A << endl;


	//cout << "m_B = " << Person::m_B << endl; //私有权限访问不到
}

int main() {

	test01();

	system("pause");

	return 0;
}
```



**示例2：**

```C++
class Person
{

public:

	//静态成员函数特点：
	//1 程序共享一个函数
	//2 静态成员函数只能访问静态成员变量
	
	static void func()
	{
		cout << "func调用" << endl;
		m_A = 100;
		//m_B = 100; //错误，不可以访问非静态成员变量
	}

	static int m_A; //静态成员变量
	int m_B; // 
private:

	//静态成员函数也是有访问权限的
	static void func2()
	{
		cout << "func2调用" << endl;
	}
};
int Person::m_A = 10;


void test01()
{
	//静态成员变量两种访问方式

	//1、通过对象
	Person p1;
	p1.func();

	//2、通过类名
	Person::func();


	//Person::func2(); //私有权限访问不到
}

int main() {

	test01();

	system("pause");

	return 0;
}
```



#### 11.this指针

**this指针指向被调用的成员函数所属的对象**



this指针是隐含每一个非静态成员函数内的一种指针

this指针不需要定义，直接使用即可



this指针的用途：

*  当形参和成员变量同名时，可用this指针来区分
*  在类的非静态成员函数中返回对象本身，可使用return *this

```C++
class Person
{
public:

	Person(int age)
	{
		//1、当形参和成员变量同名时，可用this指针来区分
		this->age = age;
	}

	Person& PersonAddPerson(Person p)
	{
		this->age += p.age;
		//返回对象本身
		return *this;
	}

	int age;
};

void test01()
{
	Person p1(10);
	cout << "p1.age = " << p1.age << endl;

	Person p2(10);
	p2.PersonAddPerson(p1).PersonAddPerson(p1).PersonAddPerson(p1);
	cout << "p2.age = " << p2.age << endl;
}

int main() {

	test01();

	system("pause");

	return 0;
}
```



#### 12.空指针访问成员函数



C++中空指针也是可以调用成员函数的，但是也要注意有没有用到this指针

如果用到this指针，需要加以判断保证代码的健壮性

**示例：**

```C++
//空指针访问成员函数
class Person {
public:

	void ShowClassName() {
		cout << "我是Person类!" << endl;
	}

	void ShowPerson() {
		if (this == NULL) {
			return;
		}
		cout << mAge << endl;
	}

public:
	int mAge;
};

void test01()
{
	Person * p = NULL;
	p->ShowClassName(); //空指针，可以调用成员函数
	p->ShowPerson();  //但是如果成员函数中用到了this指针，就不可以了
}

int main() {

	test01();

	system("pause");

	return 0;
}
```



#### 13.const修饰成员函数（常函数）

**常函数：**

* 成员函数后加const后我们称为这个函数为**常函数**
* 常函数内不可以修改成员属性
* 成员属性声明时加关键字mutable后，在常函数中依然可以修改

**常对象：**

* 声明对象前加const称该对象为常对象
* 常对象只能调用常函数



**示例：**

```C++
class Person {
public:
	Person() {
		m_A = 0;
		m_B = 0;
	}

	//this指针的本质是一个指针常量，指针的指向不可修改
	//如果想让指针指向的值也不可以修改，需要声明常函数
	void ShowPerson() const {
		//const Type* const pointer;
		//this = NULL; //不能修改指针的指向 Person* const this;
		//this->mA = 100; //但是this指针指向的对象的数据是可以修改的

		//const修饰成员函数，表示指针指向的内存空间的数据不能修改，除了mutable修饰的变量
		this->m_B = 100;
	}

	void MyFunc() const {
		//mA = 10000;
	}

public:
	int m_A;
	mutable int m_B; //可修改 可变的
};


//const修饰对象  常对象
void test01() {

	const Person person; //常量对象  
	cout << person.m_A << endl;
	//person.mA = 100; //常对象不能修改成员变量的值,但是可以访问
	person.m_B = 100; //但是常对象可以修改mutable修饰成员变量

	//常对象访问成员函数
	person.MyFunc(); //常对象不能调用const的函数

}

int main() {

	test01();

	system("pause");

	return 0;
}
```



#### 14.全局函数做友元

```C++
class Building
{
	//告诉编译器 goodGay全局函数 是 Building类的好朋友，可以访问类中的私有内容
	friend void goodGay(Building * building);

public:

	Building()
	{
		this->m_SittingRoom = "客厅";
		this->m_BedRoom = "卧室";
	}


public:
	string m_SittingRoom; //客厅

private:
	string m_BedRoom; //卧室
};


void goodGay(Building * building)
{
	cout << "好基友正在访问： " << building->m_SittingRoom << endl;
	cout << "好基友正在访问： " << building->m_BedRoom << endl;
}


void test01()
{
	Building b;
	goodGay(&b);
}

int main(){

	test01();

	system("pause");
	return 0;
}
```





示例：

```C++
class Building;
class goodGay
{
public:

	goodGay();
	void visit();

private:
	Building *building;
};


class Building
{
	//告诉编译器 goodGay类是Building类的好朋友，可以访问到Building类中私有内容
	friend class goodGay;

public:
	Building();

public:
	string m_SittingRoom; //客厅
private:
	string m_BedRoom;//卧室
};

Building::Building()
{
	this->m_SittingRoom = "客厅";
	this->m_BedRoom = "卧室";
}

goodGay::goodGay()
{
	building = new Building;
}

void goodGay::visit()
{
	cout << "好基友正在访问" << building->m_SittingRoom << endl;
	cout << "好基友正在访问" << building->m_BedRoom << endl;
}

void test01()
{
	goodGay gg;
	gg.visit();

}

int main(){

	test01();

	system("pause");
	return 0;
}
```

示例：

```C++
class Building;
class goodGay
{
public:

	goodGay();
	void visit(); //只让visit函数作为Building的好朋友，可以发访问Building中私有内容
	void visit2(); 

private:
	Building *building;
};


class Building
{
	//告诉编译器  goodGay类中的visit成员函数 是Building好朋友，可以访问私有内容
	friend void goodGay::visit();

public:
	Building();

public:
	string m_SittingRoom; //客厅
private:
	string m_BedRoom;//卧室
};

Building::Building()
{
	this->m_SittingRoom = "客厅";
	this->m_BedRoom = "卧室";
}

goodGay::goodGay()
{
	building = new Building;
}

void goodGay::visit()
{
	cout << "好基友正在访问" << building->m_SittingRoom << endl;
	cout << "好基友正在访问" << building->m_BedRoom << endl;
}

void goodGay::visit2()
{
	cout << "好基友正在访问" << building->m_SittingRoom << endl;
	//cout << "好基友正在访问" << building->m_BedRoom << endl;
}

void test01()
{
	goodGay  gg;
	gg.visit();

}

int main(){
    
	test01();

	system("pause");
	return 0;
}
```



#### 15.运算符重载（函数重载）



```c++
#define _CRT_SECURE_NO_WARNINGS
//函数重载的应用 operator+ 可以重载加号进行使用 全局函数和成员函数都可以重载+号
#include<iostream>
using namespace std;

class people
{
public:
	//成员函数的定义：
	/*people operator+ (people& p)
	{
		people temp;
		temp.m_a = p.m_a + this->m_a;
		temp.m_b = p.m_b + this->m_b;
		return temp;
	}*/

	int m_a = 15;
	int m_b = 10;
};

//全局函数的定义：重载加号使齐可以输出people的相加成员的结果
//people operator+ (people& a, people& b)
//{
//	people temp;
//	temp.m_a = a.m_a + b.m_a;
//	temp.m_b = a.m_b + b.m_b;
//	return temp;
//}

ostream & operator<< (ostream &out, people& p)
{
	cout << p.m_a << endl;
	cout << p.m_b << endl;
	return cout;
}



int main()
{
	people p1;
	people p2;

	cout << p1;
	cout << p2;



	system("pause");
	return 0;
}
```



#### 16.**继承的基本语法**

好处 ： 减少代码量：

用法：

people a ： people b

子类：父类





**继承方式一共有三种：**

* 公共继承
* 保护继承
* 私有继承





![img](E:\Download\Compressed\资料\讲义\assets\clip_image002.png)





**示例：**

```C++
class Base1
{
public: 
	int m_A;
protected:
	int m_B;
private:
	int m_C;
};

//公共继承
class Son1 :public Base1
{
public:
	void func()
	{
		m_A; //可访问 public权限
		m_B; //可访问 protected权限
		//m_C; //不可访问
	}
};

void myClass()
{
	Son1 s1;
	s1.m_A; //其他类只能访问到公共权限
}

//保护继承
class Base2
{
public:
	int m_A;
protected:
	int m_B;
private:
	int m_C;
};
class Son2:protected Base2
{
public:
	void func()
	{
		m_A; //可访问 protected权限
		m_B; //可访问 protected权限
		//m_C; //不可访问
	}
};
void myClass2()
{
	Son2 s;
	//s.m_A; //不可访问
}

//私有继承
class Base3
{
public:
	int m_A;
protected:
	int m_B;
private:
	int m_C;
};
class Son3:private Base3
{
public:
	void func()
	{
		m_A; //可访问 private权限
		m_B; //可访问 private权限
		//m_C; //不可访问
	}
};
class GrandSon3 :public Son3
{
public:
	void func()
	{
		//Son3是私有继承，所以继承Son3的属性在GrandSon3中都无法访问到
		//m_A;
		//m_B;
		//m_C;
	}
};
```



#### 17.继承中构造和析构顺序

**示例：**

```C++
class Base 
{
public:
	Base()
	{
		cout << "Base构造函数!" << endl;
	}
	~Base()
	{
		cout << "Base析构函数!" << endl;
	}
};

class Son : public Base
{
public:
	Son()
	{
		cout << "Son构造函数!" << endl;
	}
	~Son()
	{
		cout << "Son析构函数!" << endl;
	}

};


void test01()
{
	//继承中 先调用父类构造函数，再调用子类构造函数，析构顺序与构造相反
	Son s;
}

int main() {

	test01();

	system("pause");

	return 0;
}
```



#### 18.继承同名成员处理方式

* 访问子类同名成员   直接访问即可
* 访问父类同名成员   需要加作用域



**示例：**

```C++
class Base {
public:
	Base()
	{
		m_A = 100;
	}

	void func()
	{
		cout << "Base - func()调用" << endl;
	}

	void func(int a)
	{
		cout << "Base - func(int a)调用" << endl;
	}

public:
	int m_A;
};


class Son : public Base {
public:
	Son()
	{
		m_A = 200;
	}

	//当子类与父类拥有同名的成员函数，子类会隐藏父类中所有版本的同名成员函数
	//如果想访问父类中被隐藏的同名成员函数，需要加父类的作用域
	void func()
	{
		cout << "Son - func()调用" << endl;
	}
public:
	int m_A;
};

void test01()
{
	Son s;

	cout << "Son下的m_A = " << s.m_A << endl;
	cout << "Base下的m_A = " << s.Base::m_A << endl;

	s.func();
	s.Base::func();
	s.Base::func(10);

}
int main() {

	test01();

	system("pause");
	return EXIT_SUCCESS;
}
```



1. 子类对象可以直接访问到子类中同名成员
2. 子类对象加作用域可以访问到父类同名成员
3. 当子类与父类拥有同名的成员函数，子类会隐藏父类中同名成员函数，加作用域可以访问到父类中同名函数



#### 19.菱形继承类

**典型的菱形继承案例：**



![IMG_256](E:\Download\Compressed\资料\讲义\assets\clip_image002.jpg)



**菱形继承问题：**

1.     羊继承了动物的数据，驼同样继承了动物的数据，当草泥马使用数据时，就会产生二义性。

2.     草泥马继承自动物的数据继承了两份，其实我们应该清楚，这份数据我们只需要一份就可以。



**示例：**

```C++
class Animal
{
public:
	int m_Age;
};

//继承前加virtual关键字后，变为虚继承
//此时公共的父类Animal称为虚基类
class Sheep : virtual public Animal {};
class Tuo   : virtual public Animal {};
class SheepTuo : public Sheep, public Tuo {};

void test01()
{
	SheepTuo st;
	st.Sheep::m_Age = 100;
	st.Tuo::m_Age = 200;

	cout << "st.Sheep::m_Age = " << st.Sheep::m_Age << endl;
	cout << "st.Tuo::m_Age = " <<  st.Tuo::m_Age << endl;
	cout << "st.m_Age = " << st.m_Age << endl;
}


int main() {

	test01();

	system("pause");

	return 0;
}
```



* 菱形继承带来的主要问题是子类继承两份相同的数据，导致资源浪费以及毫无意义
* 利用虚继承可以解决菱形继承问题 Virturl

#### 20.多态的基本概念

多态分为两类

* 静态多态: 函数重载 和 运算符重载属于静态多态，复用函数名
* 动态多态: 派生类和虚函数实现运行时多态

静态多态和动态多态区别：

* 静态多态的函数地址早绑定  -  编译阶段确定函数地址
* 动态多态的函数地址晚绑定  -  运行阶段确定函数地址

```C++
class Animal
{
public:
	//Speak函数就是虚函数
	//函数前面加上virtual关键字，变成虚函数，那么编译器在编译的时候就不能确定函数调用了。
	virtual void speak()
	{
		cout << "动物在说话" << endl;
	}
};

class Cat :public Animal
{
public:
	void speak()
	{
		cout << "小猫在说话" << endl;
	}
};

class Dog :public Animal
{
public:

	void speak()
	{
		cout << "小狗在说话" << endl;
	}

};
//我们希望传入什么对象，那么就调用什么对象的函数
//如果函数地址在编译阶段就能确定，那么静态联编
//如果函数地址在运行阶段才能确定，就是动态联编

void DoSpeak(Animal & animal)
{
	animal.speak();
}
//
//多态满足条件： 
//1、有继承关系
//2、子类重写父类中的虚函数
//多态使用：
//父类指针或引用指向子类对象

void test01()
{
	Cat cat;
	DoSpeak(cat);


	Dog dog;
	DoSpeak(dog);
}


int main() {

	test01();

	system("pause");

	return 0;
}
```

总结：

多态满足条件

* 有继承关系
* 子类重写父类中的虚函数

多态使用条件

* 父类指针或引用指向子类对象

重写：函数返回值类型  函数名 参数列表 完全一致称为重写



案例2：

```c++
#define _CRT_SECURE_NO_WARNINGS

#include<iostream>
using namespace std;

class animal
{
public:
	virtual void saying()
	{
		cout << "animal" << endl;
	}
};

class dog:public animal
{
public:
	void saying()
	{
		cout << "dog" << endl;
	}
};


class cat:public animal
{
public:
	void saying()
	{
		cout << "cat" << endl;
	}
};

void func(animal &animal)
{
	animal.saying();
}

int main()
{
	animal a;
	cat b;
	dog d;

	func(a);
	func(b);
	func(d);


	system("pause");
	return 0;
}

```



#### 21.文件操作

c++对文件进行操作需要包含头文件<fstream>



文本类型分为两种：

1.文本文件

2.二进制文件



操作文件的三大类：

1.ofstream : 写操作

2.ifstream: : 读操作

3.fstream : 读写操作
