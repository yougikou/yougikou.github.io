---
title: "元素"
# meta title
meta_title: ""
# meta description
description: "这是元描述"
# save as draft
draft: false
---

{{< toc >}}

这是一个标题示例。您可以使用以下Markdown规则使用这些标题。例如：使用 `#` 表示标题1，使用 `######` 表示标题6。

# 标题1

## 标题2

### 标题3

#### 标题4

##### 标题5

###### 标题6

<hr>

### 强调

强调，也称为斜体，使用 *星号* 或 _下划线_。

粗体强调，使用 **星号** 或 **下划线**。

组合强调使用 **星号和_下划线_**。

删除线使用两个波浪号。~~删除这个。~~

<hr>

### 按钮

{{< button label="按钮" link="/" style="solid" >}}

<hr>

### 链接

[我是一个内联样式链接](https://www.google.com)

[我是一个带有标题的内联样式链接](https://www.google.com "Google首页")

[我是一个指向仓库文件的相对引用](../blob/master/LICENSE)

URL和尖括号中的URL会自动变成链接。
<http://www.example.com> 或 <http://www.example.com> 有时
example.com（但例如在Github上不会）。

一些文本来显示引用链接可以在后面。

<hr>

### 段落

欢迎来到元素页面。这里展示了各种页面元素的示例。您可以使用这些元素来构建丰富的内容页面。Markdown是一种轻量级标记语言，允许您使用易于阅读、易于编写的纯文本格式编写。

这个页面展示了标题、强调、链接、列表、代码块等常见元素的使用方法。您可以根据需要调整和自定义这些元素。

<hr>

### 有序列表

1. 列表项
2. 列表项
3. 列表项
4. 列表项
5. 列表项

<hr>

### 无序列表

- 列表项
- 列表项
- 列表项
- 列表项
- 列表项

<hr>

### 通知

{{< notice "note" >}}
这是一个简单的注释。
{{< /notice >}}

{{< notice "quote" >}}
这是一个简单的引用。
{{< /notice >}}

{{< notice "tip" >}}
这是一个简单的提示。
{{< /notice >}}

{{< notice "info" >}}
这是一个简单的信息。
{{< /notice >}}

{{< notice "warning" >}}
这是一个简单的警告。
{{< /notice >}}

<hr>

### 代码和语法高亮

这是一个 `行内代码` 示例。

```javascript
var s = "JavaScript语法高亮";
alert(s);
```

```python
s = "Python语法高亮"
print(s)
```

```c  { linenos=true }
#include <stdio.h>

int main(void)
{
    printf("hello, world\n");
    return 0;
}
```

<hr>

### 引用

> 您是为特定的事情而来，还是只是一般的批评？以最大曲速飞行时，您似乎瞬间出现在两个地方。

<hr>

### 表格

| 表格        |      是      |   酷 |
| ----------- | :----------: | ---: |
| 列3是       |  右对齐      | $1600 |
| 列2是       |   居中       |   $12 |
| 斑马条纹    |   很整洁     |    $1 |

<hr>